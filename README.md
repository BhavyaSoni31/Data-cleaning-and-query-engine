# LLM-Powered Flight Data Cleaning and Analysis

This project leverages advanced Large Language Models (LLMs) and supporting frameworks to clean, transform, and analyze flight booking datasets. The goal is to empower users to handle inconsistencies, fill missing values, rename columns for business-friendly querying, and perform data-driven analysis through an intuitive interface.

## Features

- **Data Cleaning**: Automated handling of missing values and inconsistent data entries.
- **Data Transformation**: Renames columns for better readability and ease of use in queries.
- **Business Intelligence**: Enables easy and effective querying of the dataset.
- **LLM Integration**: Uses OpenAI and LangChain for intelligent data manipulation.
- **Modular Design**: Designed with reusability and scalability in mind.

## File Structure

- **`main.py`**: The entry point of the application. It orchestrates the data ingestion, cleaning, and querying processes.
- **`prompts.py`**: Contains custom-designed prompts for interacting with LLMs.
- **`utils.py`**: Utility functions supporting data processing and analysis.

## Requirements

Ensure the following are installed:

- Python 3.9+
- Required Python packages (see `requirements.txt`)

### Install Required Packages

```bash
pip install -r requirements.txt
