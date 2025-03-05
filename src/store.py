import chromadb
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

DB_DIR = "data/vector_db"
chroma_client = chromadb.PersistentClient(DB_DIR)

collection = chroma_client.get_or_create_collection("financial_reports")

def clean_metadata(metadata):
    return {k: v for k,v in metadata.items() if v is not None}

def store_documents(text, metadata):

    cl_metadata = clean_metadata(metadata)
    doc_id = cl_metadata["doc_id"]
    embedding = embedding_model.embed_documents([text])[0]

    collection.add(
        ids=doc_id,
        embeddings=embedding,
        metadatas=[cl_metadata]
    )
    
    print("Document stored!")

def flush_db():
    chroma_client.delete_collection("financial_reports")