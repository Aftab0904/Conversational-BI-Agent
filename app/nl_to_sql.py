import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

def generate_sql(query):

    prompt = f"""
You are a SQL expert.

Convert the user question into SQL.

STRICT RULES:
- Return ONLY SQL
- NO markdown (no ```sql)
- NO explanation
- NO comments

Tables:
orders(order_id, user_id, order_number)
order_products(order_id, product_id, reordered)
products(product_id, product_name, aisle_id, department_id)
aisles(aisle_id, aisle)
departments(department_id, department)

Question:
{query}
"""

    response = llm.invoke(prompt).content.strip()

    #  STRONG CLEANING
    if "```" in response:
        response = response.split("```")[1]  # remove markdown block

    response = response.replace("sql", "").strip()

    return response

def generate_sql_with_reasoning(query):

    prompt = f"""
You are an expert data analyst.

Break the problem into steps, then generate SQL.

Rules:
1. First think step by step
2. Then give FINAL SQL only

Tables:
orders(order_id, user_id, order_number)
order_products(order_id, product_id, reordered, add_to_cart_order)
products(product_id, product_name, aisle_id, department_id)
aisles(aisle_id, aisle)
departments(department_id, department)

Question:
{query}
"""

    response = llm.invoke(prompt).content.strip()

    #  extract only SQL
    if "SELECT" in response:
        response = response[response.find("SELECT"):]

    if "```" in response:
        response = response.split("```")[1]

    return response.strip()