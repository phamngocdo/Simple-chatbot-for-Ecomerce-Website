import sys
import os
import json
import numpy as np

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS


def load_markdown_from_dir(dir_path):
    loader = DirectoryLoader(dir_path, glob="*.md", loader_cls=TextLoader)
    documents = loader.load()
    return [doc.page_content for doc in documents]

def serialize(obj):
    from datetime import datetime
    from decimal import Decimal
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def load_data_from_db():
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
    sys.path.append(BASE_DIR)
    from config.db import get_db_connection  

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]

    data = {}
    for table in tables:
        cursor.execute(f"SELECT * FROM {table};")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        data[table] = [dict(zip(columns, row)) for row in rows] 

    conn.close()
    return data

def get_embedding():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500, 
        chunk_overlap=50,
        separators='\n',
        length_function=len
    )


    markdown_texts = load_markdown_from_dir("src/models/docs")
    md_chunks = text_splitter.split_text("\n".join(markdown_texts))

    embedding_model = GPT4AllEmbeddings(model_file='../trained/all-MiniLM-v6-v2.F32.gguf')
    db = FAISS.from_texts(texts=md_chunks, embedding=embedding_model)
    db.save_local('../trained/vector_database')
    return db
    
# 🔥 Chạy chương trình
if __name__ == "__main__":
    get_embedding()
