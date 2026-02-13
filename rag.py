# rag.py
# @Author: Saneh Lata

from uuid import uuid4
from dotenv import load_dotenv
from pathlib import Path

#from langchain_community.document_loaders import PlaywrightURLLoader
from langchain_community.document_loaders import  WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

# ✅ langchain_chroma for LangChain 1.2.10
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

# Constants
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTORSTORE_DIR = Path(__file__).parent / "resources/vectorstore"
COLLECTION_NAME = "real_estate"

llm = None
vector_store = None


def initialize_components():
    """Initialize Langchain_Groq LLM and Chroma vector store"""
    global llm, vector_store

    # Initialize HuggingFace LLM
    if llm is None:
        print("Loading Langchain_Groq LLM...")

        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=200
        )

    # Initialize Chroma vector store
    if vector_store is None:
        print("Initializing Chroma vector store...")
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"}
        )

        vector_store = Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=str(VECTORSTORE_DIR)
        )


def process_urls(urls):
    """Scrape data from URLs and store them in vector DB"""
    yield "Initializing components..."
    initialize_components()

    yield "Resetting vector store...✅"
    vector_store.reset_collection()  # clears all existing documents

    all_docs = []

    for url in urls:
        yield f"Loading data from URL: {url}...✅"
        #loader = PlaywrightURLLoader(urls=[url])
        loader = WebBaseLoader(url)
        data = loader.load()

        yield f"Splitting text from URL: {url} into chunks...✅"
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ".", " "],
            chunk_size=CHUNK_SIZE
        )
        docs = text_splitter.split_documents(data)

        # Assign the correct URL to each chunk
        for doc in docs:
            doc.metadata["source"] = url

        all_docs.extend(docs)

    yield "Adding chunks to vector database...✅"
    uuids = [str(uuid4()) for _ in range(len(all_docs))]
    vector_store.add_documents(all_docs, ids=uuids)
    yield "Done adding documents to vector database...✅"


def generate_answer(query):
    """Retrieve answer using ChatGroq + vector store"""

    if vector_store is None:
        raise RuntimeError("Vector database is not initialized")

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    docs = retriever.invoke(query)

    # Combine retrieved context
    context = "\n\n".join([doc.page_content for doc in docs])

    # Structured Chat Prompt
    messages = [
        SystemMessage(
            content=(
                "You are a precise financial analyst.\n"
                "Answer the question using ONLY the provided context.\n"
                "Return the exact value mentioned.\n"
                "Do NOT calculate.\n"
                "Do NOT infer.\n"
                "If the answer is not in the context, say 'I don't know'."
            )
        ),
        HumanMessage(
            content=f"""
Context:
{context}

Question: {query}

Answer:
"""
        )
    ]

    # Proper ChatGroq call
    response = llm.invoke(messages)

    answer = response.content.strip()

    return answer, docs

if __name__ == "__main__":
    urls = [
        "https://www.cnbc.com/2026/02/05/billionaire-investing-family-office.html",
        "https://www.cnbc.com/2026/02/11/delinquencies-commercial-mortgage-backed-securities-rise.html"
    ]

    for msg in process_urls(urls):
        print(msg)

    answer, sources = generate_answer(
        "How much direct investments are family offices making in January 2026?"
    )
    print(f"\nAnswer: {answer}\n")
    print("Sources:")
    for doc in sources:
        print(f"- {doc.metadata.get('source', 'No source')} (length={len(doc.page_content)})")
