import os
import re
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_experimental.sql.base import SQLDatabase, SQLDatabaseChain


def remove_markdown(sql_query: str) -> str:
    """
    Strip out any triple-backtick fences (``` or ```sql … ```) from the generated SQL.
    """
    cleaned = re.sub(
        r"```(?:\w+)?\s*(.*?)\s*```",
        r"\1",
        sql_query,
        flags=re.DOTALL
    )
    return cleaned.strip()


def build_database_chain():
    # Load environment variables from .env
    load_dotenv()
    gemini_api_key = os.environ["GEMINI_API_KEY"]
    db_user        = os.environ["DB_USER"]
    db_password    = os.environ["DB_PASSWORD"]
    db_host        = os.environ["DB_HOST"]
    db_port        = os.environ["DB_PORT"]

    # Initialize the LLM with the Gemini API key
    chat_model = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.0,
        max_output_tokens=256,
        api_key=gemini_api_key,
    )

    # Custom prompt matching SQLDatabaseChain variables
    sql_prompt = PromptTemplate(
        input_variables=["input", "table_info", "dialect"],
        template="""
            Given an input question, produce a syntactically correct {dialect} SQL query.
            OUTPUT ONLY the SQL query in plain text—no markdown, code fences, or commentary.

            Question: {input}
            Schema:
            {table_info}

            SQL Query:
        """
    )

    # Build SQLAlchemy engine and SQLDatabase wrapper
    db_connection_string = (
        f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/dis_mag_system"
    )
    engine = create_engine(db_connection_string)
    db     = SQLDatabase(engine=engine)

    # Create the SQLDatabaseChain with custom prompt
    chain = SQLDatabaseChain.from_llm(
        llm=chat_model,
        db=db,
        prompt=sql_prompt,
        return_intermediate_steps=True,
    )

    return chain, engine, db


def ask_over_db(question: str):
    """
    Generate SQL for `question`, strip fences, execute it, and return both the SQL and the result rows.
    """
    chain, engine, db = build_database_chain()

    # Generate raw SQL using the chain's llm_chain
    raw_sql = chain.llm_chain.run(
        input=question,
        table_info=db.get_table_info(),
        dialect=db.dialect,
    )

    # Clean out any accidental fences
    clean_sql = remove_markdown(raw_sql)

    # Execute the cleaned SQL against the database
    try:
        with engine.connect() as conn:
            result = conn.execute(text(clean_sql))
            rows = result.fetchall()
    except Exception as e:
        print(f"Error during SQL execution: {e}")
        return None, None

    return clean_sql, rows


if __name__ == "__main__":
    question_input = (
        "What is the maximum number of workers assigned to any single incident?"
    )
    sql_response, sql_results = ask_over_db(question_input)

    if sql_response:
        print("\n=== Generated SQL ===")
        print(sql_response)
        print("\n=== Query Results ===")
        for row in sql_results:
            print(row)
    else:
        print("Failed to execute query.")
