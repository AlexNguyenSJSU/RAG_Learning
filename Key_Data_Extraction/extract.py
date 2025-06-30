import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from typing import Optional, List
from models import KeyDataExtractionRequest, ExtractedPeople

def build_extraction_chain():
    # load environment variables from .env file
    load_dotenv()
    gemini_api_key = os.environ["GEMINI_API_KEY"]

    # Initialize the LLM with the Gemini API key
    llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.0,
            max_output_tokens=128,
            api_key=gemini_api_key
        )
    
    # Define the parser for the structured output:
    parser = PydanticOutputParser(pydantic_object=KeyDataExtractionRequest)
    fmt = parser.get_format_instructions()

    # Define the chat prompt template for key information extraction
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert for key information extraction. "
                "Only extract relevant information from the text. "
                "If you do not know the value of an attribute asked to extract, "
                "return cannot-extract for the attribute's value."
                "Respond with **only** valid JSON matching the schema."
            ),
            ("system", "{format_instructions}"),
            ("human", "{text}"),
        ]
    ).partial(format_instructions=fmt)

    # Define the chain for extracting key data using the LLM
    # The schema for the structured output is defined using Pydantic models.
    chain = prompt | llm
    return chain, parser

def extract_key_data(text: str):
    try:
        """Extract key data from the input text using the defined chain."""
        chain, parser = build_extraction_chain()
        response = chain.invoke({"text": text})
        return parser.parse(response.content)
    except OutputParserException as e:
        print(f"Error parsing output: {e}")
        return None

if __name__ == "__main__":
    text_input = """I'm so impressed with this product! It has truly transformed how I approach my daily tasks. The quality exceeds my expectations, and the customer support is truly exceptional. I've already suggested it to all my colleagues and relatives. Anh Hoai Nguyen from Viet Nam recently reviewed a book she loved."""
    comment_text = "I absolutely love this product! It's been a game-changer for my daily routine. The quality is top-notch and the customer service is outstanding. I've recommended it to all my friends and family. - Sarah Johnson, USA"
    # Extract key data from the text input
    extracted_data = extract_key_data(text_input)
    print("\nExtracted Key Data:")
    print(extracted_data)
    print("\n----------\n") 
    print("Extracted Key Data from Comment:")
    extracted_data_comment = extract_key_data(comment_text)
    print(extracted_data_comment)
    print("\n----------\n")
    print("Extracted People:")
    extracted_people = ExtractedPeople(people=[extract_key_data(text_input), extract_key_data(comment_text)])
    print(extracted_people)
