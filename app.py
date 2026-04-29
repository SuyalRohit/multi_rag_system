import streamlit as st
from main import handle_query, router

st.set_page_config(page_title="RAG System", layout="wide")

st.title("🔍 Multi-RAG System (Text + SQL)")

query = st.text_input("Ask a question:", placeholder="e.g. What is an incident?")

if query:
    route = router(query)
    
    st.write(f"**Route:** {route}")

    with st.spinner("Processing..."):
        answer = handle_query(query)

    st.write("### Answer:")
    st.write(answer)