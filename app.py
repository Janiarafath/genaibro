import streamlit as st
from qa_engine import load_and_split_pdf, create_vector_store, get_answer

st.set_page_config(page_title="📄 Document Q&A - GenAI")
st.title("📄 Upload PDF and Ask Questions")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with st.spinner("Processing PDF..."):
        chunks = load_and_split_pdf(uploaded_file)
        index, all_chunks, _ = create_vector_store(chunks)
        st.success("PDF processed successfully!")

    question = st.text_input("Ask a question from the document:")
    
    if question:
        with st.spinner("Searching for answer..."):
            answer = get_answer(question, index, all_chunks)
            st.markdown(f"**Answer:** {answer}")
