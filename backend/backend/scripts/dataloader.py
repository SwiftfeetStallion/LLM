from langchain_core.documents import Document
from langchain_community.document_loaders import BSHTMLLoader
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

import re
from pathlib import Path

class DataLoader:

    def __init__(self, data_path: str, dataset_path: str, embedding_model_name: str):
        self.data_path = data_path
        self.dataset_path = dataset_path
        self.embedding_model_name = embedding_model_name

    def __clean_documents(self, docs: list[Document]):
        for document in docs:
            document.page_content = re.sub(r'(\r\n|\r|\n){2,}', r'\n', document.page_content)
            document.page_content = re.sub(r'[ \t]+', ' ', document.page_content)

    def __prepare_documents(self):
        self.documents = []
        for path in self.urls:
            loader = BSHTMLLoader(path)
            data = loader.load()
            self.__clean_documents(data)
            self.documents.extend(data)
    
    def __prepare_urls(self):
        self.urls = []
        path = Path(self.data_path)
        self.urls = [elem.resolve() for elem in path.glob("**/*.html")]
        
    def load(self):
        self.__prepare_urls()
        self.__prepare_documents()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

        docs = text_splitter.split_documents(self.documents)
        embedding_function = HuggingFaceEmbeddings(model_name=self.embedding_model_name,
                                           encode_kwargs={"normalize_embeddings": True})

        Chroma.from_documents(docs, embedding_function, persist_directory=self.dataset_path)
        
        
