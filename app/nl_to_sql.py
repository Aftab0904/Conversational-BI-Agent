import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# -------------------------------
# SCHEMA (VERY IMPORTANT)
# -------------------------------
SCHEMA = """
Tables:

orders(order_id, user_id, order_number)
order_products(order_id, product_id, reordered, add_to_cart_order)
products(product_id, product_name, aisle_id, department_id)
aisles(aisle_id, aisle)
departments(department_id, department)
"""

# -------------------------------
# FEW-SHOT EXAMPLES (BOOST ACCURACY) prompt engineering , few shot, one shot prompting
# -------------------------------
EXAMPLES = """
Example 1:
Q: most ordered products
SQL:
SELECT p.product_name, COUNT(*) as total_orders
FROM order_products op
JOIN products p ON op.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_orders DESC
LIMIT 10;

Example 2:
Q: top departments by reorder rate
SQL:
SELECT d.department,
       CAST(SUM(CASE WHEN op.reordered = 1 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS reorder_rate
FROM order_products op
JOIN products p ON op.product_id = p.product_id
JOIN departments d ON p.department_id = d.department_id
GROUP BY d.department
ORDER BY reorder_rate DESC;

Example 3:
Q: number of orders per user
SQL:
SELECT user_id, COUNT(order_id) as total_orders
FROM orders
GROUP BY user_id
ORDER BY total_orders DESC;
"""

# -------------------------------
# CLEAN FUNCTION
# -------------------------------
def clean_sql(response: str) -> str:
    if "```" in response:
        parts = response.split("```")
        if len(parts) > 1:
            response = parts[1]

    response = response.replace("sql", "").strip()

    # remove accidental text before SELECT
    if "SELECT" in response:
        response = response[response.find("SELECT"):]

    return response.strip()


# -------------------------------
# SIMPLE SQL GENERATION
# -------------------------------
def generate_sql(query):

    prompt = f"""
You are a strict SQL generator.

Your task is to convert a user question into SQL.

SCHEMA:
{SCHEMA}

EXAMPLES:
{EXAMPLES}

STRICT RULES:
- Use ONLY the tables given
- NEVER use "your_table"
- Always use correct JOIN conditions
- Return ONLY SQL
- No explanation, no markdown, no comments

User Question:
{query}
"""

    response = llm.invoke(prompt).content.strip()

    return clean_sql(response)


# -------------------------------
# ADVANCED (WITH REASONING)
# -------------------------------
def generate_sql_with_reasoning(query):

    prompt = f"""
You are an expert data analyst.

Think step by step internally, then generate SQL.

SCHEMA:
{SCHEMA}

EXAMPLES:
{EXAMPLES}

RULES:
- Use ONLY provided tables
- NEVER use "your_table"
- Ensure correct joins
- Return ONLY final SQL

User Question:
{query}
"""

    response = llm.invoke(prompt).content.strip()

    return clean_sql(response)