import streamlit as st
from dotenv import load_dotenv
import os

# Load env
load_dotenv()

from app.db import load_db
from app.nl_to_sql import generate_sql_with_reasoning
from app.query import run_query_with_retry
from app.visualize import auto_plot
from langchain_groq import ChatGroq

# -------------------------------
# PAGE SETUP
# -------------------------------
st.set_page_config(page_title="Conversational BI Agent", layout="wide")
st.title("Conversational BI Agent")

st.info("Ask data-related questions like: 'Top 10 products' or 'Top departments by reorder rate'")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.title(" Settings")
st.sidebar.markdown("### Example Queries:")
st.sidebar.write("• Top 10 products")
st.sidebar.write("• Top departments by reorder rate")
st.sidebar.write("• Most ordered products")

# -------------------------------
# MEMORY
# -------------------------------
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# -------------------------------
# LOAD DATABASE
# -------------------------------
con = load_db()

# -------------------------------
# LLM SETUP
# -------------------------------
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

# -------------------------------
# USER INPUT
# -------------------------------
query = st.text_input("Ask your question:")

if st.button("Run"):

    # -------------------------------
    # HANDLE FOLLOW-UP MEMORY
    # -------------------------------
    full_query = query

    if "now" in query.lower() or "that" in query.lower():
        full_query = st.session_state.last_query + " " + query

    # Save last query
    st.session_state.last_query = full_query

    st.write("🧠 Interpreted Query:", full_query)

    # -------------------------------
    # GENERATE SQL
    # -------------------------------
    sql = generate_sql_with_reasoning(full_query)

    st.subheader("Generated SQL")
    st.code(sql, language="sql")

    # -------------------------------
    # RUN QUERY (WITH SPINNER 🔥)
    # -------------------------------
    with st.spinner("Processing query..."):
        result = run_query_with_retry(con, sql, full_query, llm)

    # -------------------------------
    # DISPLAY RESULT
    # -------------------------------
    st.subheader("Result Table")

    if isinstance(result, str):
        st.error(result)
    else:
        st.dataframe(result)

        # -------------------------------
        # AUTO VISUALIZATION
        # -------------------------------
        st.subheader("Visualization")

        fig = auto_plot(result)

        if fig:
            st.pyplot(fig)
        else:
            st.info("No suitable chart for this query.")