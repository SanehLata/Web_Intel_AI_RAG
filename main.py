# @Author: Saneh Lata

import streamlit as st
from rag import process_urls, generate_answer

st.title("Web Intelligence Retrieval System (WIRS)")

# Initialize session state variables

# Initialize session state variables
if "answer" not in st.session_state:
    st.session_state.answer = ""
if "sources" not in st.session_state:
    st.session_state.sources = []
if "question" not in st.session_state:
    st.session_state.question = ""

url1 = st.sidebar.text_input("URL 1")
url2 = st.sidebar.text_input("URL 2")
url3 = st.sidebar.text_input("URL 3")

placeholder = st.empty()

process_url_button = st.sidebar.button("Process URLs")
if process_url_button:
    urls = [url for url in (url1, url2, url3) if url!='']
    if len(urls) == 0:
        placeholder.text("You must provide at least one valid url")
    else:
        # Clear previous answer and sources
        st.session_state.answer = ""
        st.session_state.sources = []
        st.session_state.question = ""

        for status in process_urls(urls):
            placeholder.text(status)

query = st.text_input("Question", value=st.session_state.question, key="question")
if query:
    try:
        # Get answer and document chunks
        answer, docs = generate_answer(query)

        st.header("Answer:")
        st.write(answer)

        # Extract unique sources only
        if docs:
            unique_sources = list({doc.metadata.get("source", "No source") for doc in docs})
            st.subheader("Sources:")
            for source in unique_sources:
                st.write(source)

    except RuntimeError as e:
        placeholder.text("You must process urls first")
