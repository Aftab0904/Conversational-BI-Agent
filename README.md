# Conversational BI Agent

![UI](assets/sql.png)

This project is an AI-powered BI system that converts natural language queries into SQL and generates insights from structured data.

## Features
- Natural Language to SQL
- Multi-step reasoning for complex queries
- Automatic retry on SQL errors
- Basic visualization
- Conversational memory

## Tech Stack
- Python
- DuckDB
- Streamlit
- Groq LLM

## Dataset
data is available for free
Download dataset from:
https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis
files inside:
data/
## How to Run
1. Create virtual environment
2. Install requirements
3. Add .env file with GROQ_API_KEY
4. Run: streamlit run app/ui.py

