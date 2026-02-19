"""
Vector Store Initialisation
"""
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer


def init_vectorstore():
    """Initialise Chroma db vector store with an educational content collection"""
    with open("data/educational_urls.txt", "r", encoding='UTF-8') as f:
        urls = f.read().splitlines()

    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=100, chunk_overlap=50
    )
    docs_list = text_splitter.split_documents(docs_list)
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=250, chunk_overlap=50
    )
    doc_splits = text_splitter.split_documents(docs_list)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(docs_list)
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="educational_content",
        embedding=embeddings
    )

    return vectorstore.as_retriever()

retriever = init_vectorstore()
