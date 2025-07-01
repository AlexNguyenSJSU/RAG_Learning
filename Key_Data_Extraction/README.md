# Sentiment Analysis App

This project provides an efficient way to analyze text and classify it as positive, negative, or neutral using Google Gemini Flash via LangChain.

## Features

* **Natural Language Understanding**: Uses Google Gemini Flash for high-quality sentiment classification.
* **Structured Pipeline**: Clear separation between preprocessing, sentiment engines, and output formatting.
* **Error Handling**: Provides clear messages on processing errors, etc.

## Requirements

* **Python** >= 3.9
* **Poetry** for dependency management
* **Google Gemini API key** (set as `GEMINI_API_KEY` in `.env`)

## Installation

1. **Clone the repository**

   ```bash
   git clone ...
   cd sentiment_analysis
   ```
2. **Install dependencies**

   ```bash
   poetry install
   ```

## Configuration

1. **Set variables in `.env`**:

   ```dotenv
   GEMINI_API_KEY=your_gemini_api_key
   ```

### Command-Line

```bash
poetry run python sentiment_analysis.py
```

## Project Structure

```text
sentiment_analysis/
├── .env                   # Environment variables
├── models.py              # Structured ouput format in Pydantic object 
├── gitignore              # Ignore files
├── sentiment_analysis.py  # Main script
├── pyproject.toml         # Poetry project file
└── README.md              # Project documentation
```

## Extending the App

* **Custom Engines**: Add new `Analyzer` subclasses for custom ML/DL models.
* **Aspect-Based Analysis**: Integrate PyABSA or similar frameworks for fine-grained insights.
* **Additional Formats**: Plug in new data loaders for file inputs (CSV, JSON, etc.).

## Contributing

1. Fork the repo and create a new branch:

   ```bash
   git checkout -b feature/YourFeature
   ```
2. Commit your changes:

   ```bash
   git commit -m "Add feature description"
   ```
3. Push and open a PR:

   ```bash
   git push origin feature/YourFeature
   ```

Include tests for new functionality and follow existing style conventions.

---

Built with ❤️ using [LangChain](https://github.com/langchain-ai/langchain) and Google Gemini Flash.
