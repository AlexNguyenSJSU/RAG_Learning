# Key Data Extraction with Google Gemini & LangChain

This project demonstrates how to extract key information (name, lastname, country) from unstructured text using Google Gemini Flash (via LangChain) and Pydantic models for structured output.

## Features

- Uses Google Gemini Flash LLM for text analysis.
- Extracts structured data (name, lastname, country) from free-form text.
- Handles both single and multiple person mentions.
- Robust output parsing with error handling.
- Easily extensible for more fields or different extraction tasks.

## Requirements

- Python 3.10+
- [Poetry](https://python-poetry.org/) for dependency management
- Google Gemini API key (set as `GEMINI_API_KEY` in your `.env` file)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd Key_Data_Extraction

2. **Install dependencies:**
   ```bash
   poetry install
   ```
   This will create a virtual environment and install all required packages defined in your `pyproject.toml`.

---

## Configuration

1. **Create a **``** file in the project root:**
   ```dotenv
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
2. **Load environment variables:** Poetry automatically picks up your `.env` when you run commands with `poetry run`. If you need to load it manually, you can use [python-dotenv](https://pypi.org/project/python-dotenv/):
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

---

## Usage

You can run the extractor against any plain-text input. Here’s a quick example:

```bash
poetry run python main.py --input-file examples/input.txt --output-file examples/output.json
```

This will:

- Read `examples/input.txt` (unstructured text).
- Extract `name`, `lastname`, and `country` for each person mentioned.
  
---

## Project Structure

```text
Key_Data_Extraction/
├── extract.py       # Core LangChain + Gemini flash logic
├── models.py          # Pydantic models for structured output
├── pyproject.toml     # Poetry config & dependencies
├── poetry.lock        # Locked dependency graph
├── .env.example       # Sample env-file with required keys
└── README.md          # Project documentation
```

---

## Extending the Extractor

- **New fields:**

  1. Update your Pydantic schema in `models.py` with the new field.
  2. Adjust the prompting logic in `extractor.py` to include instructions for the new field.

- **Alternative output formats:**

  - You can easily swap JSON for CSV by post-processing the Pydantic `.dict()` or `.json()` output.

---

## Contributing

1. **Fork** the project and create your feature branch (`git checkout -b feature/YourFeature`).
2. **Commit** your changes (`git commit -m 'Add some feature'`).
3. **Push** to the branch (`git push origin feature/YourFeature`).
4. **Open a Pull Request**.

Please make sure to run tests before submitting, and follow the existing code style.

---

## Acknowledgements

- Built with ❤️ using [LangChain](https://github.com/langchain-ai/langchain) and Google Gemini Flash.
- Inspired by traditional NLP best practices and the vibrant open-source community.

Happy extracting! 🚀
