import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain import hub
from langchain_pinecone import PineconeVectorStore

load_dotenv()


def ingest(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(
        chunk_size=300, chunk_overlap=30, separator="\n"
    )
    docs = text_splitter.split_documents(documents=documents)
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    print("Ingesting...")
    PineconeVectorStore.from_documents(
        docs, embeddings, index_name=os.environ.get("INDEX_NAME")
    )
    print("Finish")
