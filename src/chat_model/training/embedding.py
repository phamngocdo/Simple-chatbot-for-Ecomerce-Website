from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
class Embedding:
    def __init__(self):
        pass

    def load_markdown_from_dir(self, dir_path):
        loader = DirectoryLoader(dir_path, glob="*.md", loader_cls=TextLoader)
        documents = loader.load()
        return [doc.page_content for doc in documents]

    def get_embedding(self, markdown_dir="../models/docs", save_path="../src/models/trained/vector_database"):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512, 
            chunk_overlap=50,
            separators='\n',
            length_function=len
        )

        markdown_texts = self.load_markdown_from_dir(markdown_dir)
        md_chunks = text_splitter.split_text("\n".join(markdown_texts))

        embedding_model = GPT4AllEmbeddings(model_file='../trained/all-MiniLM-v6-v2.F32.gguf')
        db = FAISS.from_texts(texts=md_chunks, embedding=embedding_model)
        db.save_local(save_path)
        return db
