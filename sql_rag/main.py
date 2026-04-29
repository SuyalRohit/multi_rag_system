from .database import run_query, get_schema
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

DEBUG = False

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise Exception("GROQ_API_KEY not found")

client = Groq(api_key=groq_api_key)

def run_sql_rag(query):
    schema = get_schema()

    prompt = f"""
You are a SQL expert.

Use ONLY the schema below.

IMPORTANT RULES:
- Use only columns that exist in the schema
- Do NOT invent tables or columns
- Do NOT assume relationships unless explicitly defined
- If unsure, use a simple query instead of JOIN

Schema:
{schema}

Return ONLY a valid SQL SELECT query.
Do NOT use markdown or backticks.

Question:
{question}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    sql_query = response.choices[0].message.content.strip()
    sql_query = clean_sql(sql_query)

    # print("\nGenerated SQL:\n", sql_query)

    if not sql_query.lower().startswith("select"):
        raise Exception("Only SELECT queries allowed")
    try:
        result = run_query(sql_query)
    except Exception as e:
        return f"SQL Error: {str(e)}"
    
    # print("\nRaw Result:\n", result)

    explain_prompt = f"""
You are a helpful assistant.

Question:
{question}

SQL Query:
{sql_query}

SQL Result:
{result}

Explain the answer in a clear and simple sentence.
"""

    final_response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": explain_prompt}]
    )

    final_answer = final_response.choices[0].message.content.strip()
    if DEBUG:
        print("\nGenerated SQL:\n", sql_query)
        print("\nSQL Result:\n", final_answer)
    
    return final_answer


def clean_sql(sql):
    sql = sql.strip()

    if sql.startswith("```"):
        sql = sql.replace("```sql", "").replace("```", "").strip()

    return sql