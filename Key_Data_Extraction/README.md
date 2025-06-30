# Natural Language to SQL Converter with Google Gemini & LangChain

This project demonstrates how to convert natural language questions into SQL queries to retrieve answers from a structured MySQL database using Google Gemini Flash (via LangChain), SQLAlchemy for database connectivity, and a simple regex-based cleanup for robust execution.

## Features

* **Natural Language Understanding**: Leverages Google Gemini Flash for high-quality language-to-SQL translation.
* **Structured Prompting**: Customizable prompt templates to enforce plain-text SQL output without markdown or code fences.
* **SQL Execution**: Automatic execution of generated SQL against a local or remote MySQL database.
* **Result Display**: Prints query results in a readable tabular format in the console.
* **Error Handling**: Cleans up formatting anomalies (e.g., stray markdown fences) and reports SQL or connection errors clearly.
* **Extensible**: Easy to swap in a different LLM, database, or output parser.

## Requirements

* **Python** 3.10 or higher
* **Poetry** for dependency management
* **MySQL Server** 8.x running locally or accessible over the network
* **Google Gemini API key** (set as `GEMINI_API_KEY` in your `.env`)

## Installation

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd Ask_Over_a_DB
   ```
2. **Install dependencies**

   ```bash
   poetry install
   ```

## Configuration

1. **Copy the example environment file**

   ```bash
   cp .env.example .env
   ```
2. **Edit `.env`** with your credentials and connection info:

   ```dotenv
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   DB_USER=your_mysql_username
   DB_PASSWORD=your_mysql_password
   DB_HOST=your_MySQL_host_IP
   DB_PORT=your_default_MySQL_port    
   ```

## Usage

Run the main script to start the natural-language-to-SQL converter:

```bash
poetry run python ask_over_a_DB.py
```

You'll be prompted (or can edit the script) to input a question. The tool will:

1. Load your environment variables.
2. Initialize Google Gemini Flash via LangChain.
3. Generate a plain-text SQL query for your question.
4. Clean the SQL of any accidental markdown.
5. Execute it against your `dis_mag_system` database.
6. Print both the generated SQL and the results to the console.

### Example

```bash
> poetry run python ask_over_a_DB.py

In the table `emergency_worker`, what are the names of all columns?

=== Generated SQL ===
SHOW COLUMNS FROM emergency_worker;

=== Query Results ===
('Field', 'Type', 'Null', 'Key', 'Default', 'Extra')
('id', 'int', 'NO', 'PRI', None, 'auto_increment')
('first_name', 'varchar(50)', 'YES', '', None, '')
('last_name', 'varchar(50)', 'YES', '', None, '')
...
```

## Project Structure

```text
Ask_Over_a_DB/
├── ask_over_a_DB.py       # Main script: builds the chain, generates and runs SQL
├── .env.example          # Template for environment variables
├── pyproject.toml        # Poetry project definition and dependencies
├── poetry.lock           # Locked dependency graph
└── README.md             # Project documentation (this file)
```

## Extending the Converter

1. **New LLM**: Swap out the `ChatGoogleGenerativeAI` class for another LangChain-compatible LLM (e.g., OpenAI, Azure OpenAI).
2. **Different Database**: Change the SQLAlchemy URI to connect to PostgreSQL, SQLite, or another supported database.
3. **Enhanced Output Parsing**: Integrate Pydantic or a JSON-based `StructuredOutputParser` to enforce schema on the LLM output before execution.
4. **Web Interface**: Wrap `ask_over_a_DB.py` in a FastAPI or Streamlit app for interactive web-based querying.

## Contributing

1. **Fork** the repository and create your feature branch:

   ```bash
   git checkout -b feature/YourFeature
   ```
2. **Commit** your changes:

   ```bash
   git commit -m "Add new feature"
   ```
3. **Push** to your branch:

   ```bash
   git push origin feature/YourFeature
   ```
4. **Open a Pull Request**

Please ensure your changes include tests where applicable and maintain code style consistency.

---

Built with ❤️ using [LangChain](https://github.com/langchain-ai/langchain) and Google Gemini Flash.
