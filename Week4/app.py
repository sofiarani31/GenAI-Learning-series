
import streamlit as st

from src.pdf_loader import extract_text
from src.chunker import create_chunks
from src.embeddings import get_embeddings
from src.vector_store import store_chunks, delete_by_document
from src.rag_chain import generate_answer
from src.utils import save_uploaded_file, clear_uploads_folder

st.title("Chat With Your PDFs")

uploaded_files = st.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if "indexed_files" not in st.session_state:
    st.session_state.indexed_files = set()

if "messages" not in st.session_state:
    st.session_state.messages = []

if st.button("Index Documents", disabled=not uploaded_files):

    with st.spinner("Indexing documents..."):
        
        clear_uploads_folder()

        for pdf in uploaded_files:
            try:
                file_path = save_uploaded_file(pdf)

                if pdf.name in st.session_state.indexed_files:
                    delete_by_document(pdf.name)

                pages = extract_text(file_path)
                chunks = create_chunks(pages)

                texts = [c["text"] for c in chunks]
                embeddings = get_embeddings(texts)

                store_chunks(chunks, embeddings, pdf.name)

                st.session_state.indexed_files.add(pdf.name)

            except ValueError as e:
                st.warning(f"⚠️ Skipped {pdf.name}: {e}")

            except Exception as e:
                st.error(f"❌ Error indexing {pdf.name}: {e}")

        st.success("Documents Indexed")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        
        if msg.get("sources"):
            with st.expander("View Sources"):
                for source in msg["sources"]:
                    page = source["metadata"].get("page", "N/A")
                    st.markdown(f"**{source['metadata']['document']} — Page {page}**")
                    st.write(source["metadata"]["text"])

question = st.chat_input("Ask a question")

if question:

    st.session_state.messages.append({"role": "user", "content": question})

    with st.chat_message("user"):
        st.write(question)

    answer, sources = generate_answer(
        question,
        chat_history=st.session_state.messages[:-1]
    )

    st.session_state.messages.append({
        "role": "assistant", 
        "content": answer,
        "sources": sources
    })

    with st.chat_message("assistant"):
        st.write(answer)
        
        if sources:
            with st.expander("View Sources"):
                for source in sources:
                    page = source["metadata"].get("page", "N/A")
                    st.markdown(f"**{source['metadata']['document']} — Page {page}**")
                    st.write(source["metadata"]["text"])