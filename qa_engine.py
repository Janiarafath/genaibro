import os
import faiss
import pickle
import torch
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import pipeline

# Load embedding model
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # light & fast

# Load QA model (small to run on CPU)
qa_model = pipeline("text2text-generation", model="google/flan-t5-xl")

# Load and split PDF
def load_and_split_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    raw_text = ""
    for page in reader.pages:
        raw_text += page.extract_text() or ""
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
    chunks = splitter.split_text(raw_text)
    return chunks

# Embed and store in FAISS
def create_vector_store(chunks):
    embeddings = embedding_model.encode(chunks)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, chunks, embeddings

# Query and get answer
def get_answer(query, index, chunks):
    query_vec = embedding_model.encode([query])
    D, I = index.search(query_vec, k=3)
    retrieved = [chunks[i] for i in I[0]]
    context = " ".join(retrieved)
    
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    output = qa_model(prompt, max_length=100, do_sample=False)[0]['generated_text']
    return output
