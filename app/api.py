from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import pandas as pd
from dotenv import load_dotenv
import asyncio

# Existing logic imports
from db import load_db
from nl_to_sql import generate_sql_with_reasoning
from query import run_query_with_retry
from langchain_groq import ChatGroq

load_dotenv()

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global components
con = load_db()
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0
)

class ChatRequest(BaseModel):
    query: str
    last_query: str = ""

class ChatResponse(BaseModel):
    query: str
    sql: str
    data: list
    columns: list
    summary: str
    suggestions: list

async def generate_suggestions(query: str, df_summary: str):
    """Generates 3 contextual follow-up questions."""
    prompt = f"""
    Based on the following user query and the summary of the data returned, suggest 3 highly relevant follow-up questions the user might want to ask next.
    User Query: {query}
    Data Summary: {df_summary}
    
    Return ONLY a list of 3 questions, one per line, starting with a bullet point.
    """
    try:
        response = await asyncio.to_thread(llm.invoke, prompt)
        suggestions = [line.strip("- ").strip() for line in response.content.strip().split("\n") if line.strip()]
        return suggestions[:3]
    except Exception as e:
        print(f"Error generating suggestions: {e}")
        return ["Tell me more about this data", "Can you visualize this differently?", "What are the trends here?"]

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Handle context
        full_query = request.query
        if "now" in request.query.lower() or "that" in request.query.lower():
            full_query = request.last_query + " " + request.query
        
        # 1. Generate SQL
        sql = await asyncio.to_thread(generate_sql_with_reasoning, full_query)
        
        # 2. Execute Query
        result = await asyncio.to_thread(run_query_with_retry, con, sql, full_query, llm)
        
        if isinstance(result, str):
            raise HTTPException(status_code=400, detail=result)
        
        # 3. Process Data for JSON
        df = result
        data_json = df.to_dict(orient="records")
        columns = df.columns.tolist()
        df_summary = df.head(5).to_string()
        
        # 4. Generate Narrative Summary
        summary_prompt = f"Briefly summarize the key takeaway from this data in 2 sentences. Context: {full_query}. Data: {df_summary}"
        summary_response = await asyncio.to_thread(llm.invoke, summary_prompt)
        summary = summary_response.content
        
        # 5. Generate Suggestions
        suggestions = await generate_suggestions(full_query, df_summary)
        
        return ChatResponse(
            query=full_query,
            sql=sql,
            data=data_json,
            columns=columns,
            summary=summary,
            suggestions=suggestions
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
