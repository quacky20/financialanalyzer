import chromadb
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import os

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

DB_DIR = "../data/vector_db"
chroma_client = chromadb.PersistentClient(DB_DIR)

collection = chroma_client.create_collection("financial_reports")

def store_documents(text, metadata):
    doc_id = metadata["doc_id"]
    embedding = embedding_model.embed_documents([text])[0]

    collection.add(
        ids=doc_id,
        embeddings=embedding,
        metadatas=metadata
    )
    
    print("Document stored!")
