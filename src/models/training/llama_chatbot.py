from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader, DirectoryLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import GPT4AllEmbeddings


class LlamaChatBot:
    def __init__(self, model_path, vector_word_path):
        self.model_path = model_path
        self.word_path = vector_word_path
    
    def word_embedded(self, text=None):
        text_splitter = RecursiveCharacterTextSplitter(
            separators='\n',
            chunk_size=500,
            chunk_overlap=50,
            length_function=len
        )

        chunks = text_splitter.split_text(text=text)
    