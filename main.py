from groq import Groq
import os
from dotenv import load_dotenv

from text_rag.main import run_text_rag
from sql_rag.main import run_sql_rag

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise Exception("GROQ_API_KEY not found")

client = Groq(api_key=groq_api_key)


DEBUG = False

def router(query):
    q = query.lower()

    needs_sql = any(k in q for k in [
        "count", "total", "sum", "how many", "average"
    ])

    needs_text = any(k in q for k in [
        "what is", "why", "explain", "define"
    ])

    if needs_sql and needs_text:
        return "both"
    elif needs_sql:
        return "sql"
    elif needs_text:
        return "text"
    else:
        return "both"


def combine(query, sql_result, text_result):
    prompt = f"""
You are a helpful assistant.

Answer the question using BOTH sources below.

Question:
{query}

Structured Data (SQL Result):
{sql_result}

Context (Text RAG):
{text_result}

Instructions:
- Use both sources if relevant
- If one source is missing or unclear, still answer using the other
- Combine them into a single clear answer

Final Answer:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def handle_query(query):
    route = router(query)

    if DEBUG:
        print(f"[ROUTE]: {route}")
    if route == "sql":
        return run_sql_rag(query)

    elif route == "text":
        return run_text_rag(query)

    else:
        # split query into parts
        parts = query.split(" and ")

        sql_part = None
        text_part = None

        for part in parts:
            p = part.lower()
            if any(k in p for k in ["count", "how many", "total"]):
                sql_part = part
            else:
                text_part = part

        sql_result = run_sql_rag(sql_part) if sql_part else ""
        text_result = run_text_rag(text_part) if text_part else ""

        return combine(query, sql_result, text_result)

if __name__ == "__main__":
    while True:
        q = input("\nAsk: ")
        if q.lower() in ["exit", "quit"]:
            break

        answer = handle_query(q)
        print("\nAnswer:\n", answer)