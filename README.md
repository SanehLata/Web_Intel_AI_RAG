# Web_Intel_AI_RAG
Web Intel AI RAG is an AI-powered Web Intelligence Retrieval-Augmented Generation (RAG) application that extracts, processes, and answers questions from web content using modern LLM and embedding technologies.  The project combines web scraping, vector search, and large language models to deliver intelligent, context-aware responses based on real-time web data.


## 🚀 Features

#### 🌐 Web Content Ingestion
  Scrapes and processes web pages using BeautifulSoup and langchain's Document Loader(WebBaseLoader) and Text Splitters.
      
####  📚 Semantic Search with Vector Database
Stores embeddings in ChromaDB for fast similarity search.

#### 🤖 LLM-Powered Question Answering
Uses Groq + LangChain for generating contextual answers.

#### 🔎 HuggingFace Embeddings
Uses Sentence Transformers for high-quality semantic embeddings.

#### 🖥 Streamlit Interface
Interactive UI for querying and exploring results.



## 🏗 Tech Stack

LangChain 1.2.10

ChromaDB

Sentence Transformers

HuggingFace Hub

Groq LLM

Streamlit

BeautifulSoup4

Python-dotenv



## ⚙️ How It Works

1. A user provides a URL or content source.

2. The system extracts and cleans the content.

3. Text is split into chunks.

4. Embeddings are generated using HuggingFace models.

5. Embeddings are stored in Chroma vector database.

6. User questions are matched against relevant chunks.

7. Groq LLM generates an answer using retrieved context.

## ⚙️ Logical Architecture

```graphql
                    ┌──────────────────────┐
                    │        USER          │
                    │  Streamlit Frontend │
                    │  (main.py)          │
                    └─────────┬──────────┘
                              │
                 URL Input    │ Question Input
                              │
                              ▼

                ┌────────────────────────────┐
                │   Streamlit Application    │
                │                            │
                │ process_urls()            │
                │ generate_answer()        │
                └─────────┬────────────────┘
                          │
                          │
         ┌────────────────┴─────────────────┐
         │                                  │
         ▼                                  ▼

┌──────────────────────┐          ┌──────────────────────┐
│   WebBaseLoader      │          │     Retriever        │
│  (LangChain)         │          │  Chroma Vector DB    │
│                      │          │                      │
│ Loads Web Pages      │          │ Top-K search        │
└─────────┬────────────┘          └─────────┬────────────┘
          │                                 │
          ▼                                 ▼

┌──────────────────────┐          ┌──────────────────────┐
│ RecursiveCharacter   │          │   Context Builder    │
│ TextSplitter         │          │                      │
│                      │          │ Combine chunks       │
│ Creates chunks       │          │                      │
└─────────┬────────────┘          └─────────┬────────────┘
          │                                 │
          ▼                                 ▼

┌──────────────────────┐          ┌──────────────────────┐
│ HuggingFace          │          │ ChatGroq LLM         │
│ Embeddings           │          │ llama-3.3-70b        │
│ all-MiniLM-L6-v2     │          │                      │
└─────────┬────────────┘          └─────────┬────────────┘
          │                                 │
          ▼                                 ▼

┌─────────────────────────────────────────────┐
│           Chroma Vector Database           │
│                                             │
│ Stores:                                     │
│ • embeddings                                │
│ • document chunks                           │
│ • source metadata                           │
│                                             │
│ Persisted locally                           │
└─────────────────────────────────────────────┘
                    │
                    ▼

             ┌──────────────┐
             │   Response   │
             │ Answer +     │
             │ Sources      │
             └──────────────┘
                    │
                    ▼

             ┌──────────────┐
             │  Streamlit   │
             │   UI Output  │
             └──────────────┘


```

## ⚙️ Major pipelines
### 1. Ingestion Pipeline

```graphql
User URLs
   ↓
WebBaseLoader
   ↓
Text Splitter
   ↓
Embeddings
   ↓
Chroma Vector DB


```

### 2. Query Pipeline

```graphql
User Question
   ↓
Chroma Retriever
   ↓
Context Retrieval
   ↓
ChatGroq LLM
   ↓
Answer
   ↓
Streamlit UI

```

## 🎯 Use Cases

1. Web research assistant

2. Knowledge extraction from documentation

3. AI-powered Q&A over custom web sources

4. Prototype for production RAG systems
