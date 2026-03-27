def run_query_with_retry(con, sql, query, llm):

    try:
        df = con.execute(sql).df()
        return df

    except Exception as e:

        error_msg = str(e)

        retry_prompt = f"""
The SQL query failed.

Query:
{sql}

Error:
{error_msg}

Fix the SQL.
Return ONLY corrected SQL.
"""

        new_sql = llm.invoke(retry_prompt).content.strip()

        new_sql = new_sql.replace("```", "").replace("sql", "").strip()

        try:
            return con.execute(new_sql).df()
        except Exception as e2:
            return f" Failed after retry: {str(e2)}"