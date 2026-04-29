# Multi-RAG System (Text + SQL)

This project implements a hybrid Retrieval-Augmented Generation (RAG) system that combines:

- Text-based RAG over documents (PDFs)
- SQL-based RAG over structured data (SQLite)
- An orchestrator that routes queries to the appropriate system or both

The goal is to demonstrate how multiple knowledge sources can be integrated into a single question-answering system.

---

## Project Structure

rag-system/
├── text_rag/
│   ├── ingest.py
│   ├── main.py
│   ├── data/              # place PDF files here
│   └── chroma_db/         # generated (ignored in git)
│
├── sql_rag/
│   ├── database.py
│   ├── main.py
│   └── database/
│        ├── sql_details.txt   # schema + sample data
│        └── mydb.db           # generated (ignored in git)
│
├── app.py                 # Streamlit UI
├── main.py                # Orchestrator
├── .env
└── requirements.txt

---

## Features

- Text RAG using embeddings and vector search (ChromaDB)
- SQL RAG using LLM-generated queries over SQLite
- Hybrid routing (rule-based + LLM-assisted)
- Query decomposition for multi-intent queries
- Streamlit UI for interactive usage

---

## Setup

### 1. Clone the repository

git clone <your-repo-url>
cd rag-system

---

### 2. Create and activate virtual environment

python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows

---

### 3. Install dependencies

pip install -r requirements.txt

---

### 4. Set environment variables

Create a `.env` file in the root directory:

GROQ_API_KEY=your_api_key_here

---

## Text RAG Setup

### Add documents

Place your PDF files inside:

text_rag/data/

---

### Run ingestion

python text_rag/ingest.py

This will:
- Load PDFs
- Split into chunks
- Create embeddings
- Store them in `chroma_db/`

---

## SQL RAG Setup

### Initialize database (recommended)

python sql_rag/init_db.py

This will:
- Create a SQLite database
- Load schema and sample data from `sql_details.txt`

---

### Important

- `sql_details.txt` defines your schema and sample data
- The schema must match what is defined in `get_schema()` inside `database.py`

---

## Using Your Own Database

If you want to use your own SQLite database:

1. Replace:
   sql_rag/database/mydb.db

2. Update schema in:
   sql_rag/database.py → `get_schema()`

Note:
The schema string must match your actual database structure.  
Otherwise SQL generation may fail or produce incorrect queries.

---

## Running the System

### CLI Mode

python main.py

Example queries:

What is an incident?
How many customers are active?
What is an incident and how many customers are active?

---

### Streamlit UI

streamlit run app.py

---

## How It Works

### Routing

The system classifies queries into:
- text → document-based retrieval
- sql → structured database queries
- both → multi-source queries

---

### SQL RAG

1. LLM generates SQL from schema
2. Query is executed against SQLite
3. Result is converted into natural language

---

### Text RAG

1. Query is embedded
2. Relevant chunks retrieved from vector DB
3. LLM generates answer based on context

---

### Combined Mode

For multi-intent queries:
- Query is split into sub-parts
- Each part is routed separately
- Results are combined using LLM

---

## Limitations

- Rule-based routing is heuristic and may fail for complex queries
- SQL generation may produce invalid joins or incorrect queries
- Data sources are not fully semantically aligned
- Query splitting is currently keyword-based

---

## Future Improvements in Upcoming Version

- Replace rule-based routing with LLM-based classification
- Improve SQL query validation and retry logic
- Add schema-aware reasoning for SQL generation
- Improve query decomposition using LLM
- Add response streaming in UI
- Add evaluation and logging

---

## Notes

- `chroma_db/` and `database/` are ignored in version control
- `.env` file is not included for security reasons
- Designed as a prototype for demonstrating multi-source RAG
