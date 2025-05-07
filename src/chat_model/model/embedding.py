from pathlib import Path
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import Tool, tool
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
TRAINED_DIR = Path(__file__).resolve().parent.parent / "trained"

def load_markdown_from_dir(dir_path):
    loader = DirectoryLoader(str(dir_path), glob="*.md", loader_cls=TextLoader)
    documents = loader.load()
    return [doc.page_content for doc in documents]

def embedding_data(markdown_dir=DOCS_DIR, save_path=TRAINED_DIR / "vector_words" / "from_guides"):
    if save_path.exists():
        latest_file_time = max([f.stat().st_mtime for f in markdown_dir.glob("*.md")])
        vector_db_time = save_path.stat().st_mtime 

        if latest_file_time <= vector_db_time:
            return FAISS.load_local(str(save_path)) 

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512, 
        chunk_overlap=50,
        separators='\n',
        length_function=len
    )

    markdown_texts = load_markdown_from_dir(markdown_dir)
    md_chunks = text_splitter.split_text("\n".join(markdown_texts))

    embedding_model = GPT4AllEmbeddings(model_file=TRAINED_DIR / "all-MiniLM-L6-v2.F32.gguf")
    db = FAISS.from_texts(texts=md_chunks, embedding=embedding_model)
    
    db.save_local(str(save_path))
    return db

embedding_data()