import os
import streamlit as st

from src.index_documents import index_documents
from src.retrieval.search import semantic_search

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

if "chunks_indexed" not in st.session_state:
    st.session_state["chunks_indexed"] = 0

st.set_page_config(
    page_title="Semantic Search Engine",
    layout="wide"
)

st.title(
    "Semantic Search Engine"
)

tab1, tab2 = st.tabs(
    [
        "Upload & Index",
        "Search"
    ]
)

# -----------------------
# Upload Tab
# -----------------------

with tab1:

    uploaded_files = st.file_uploader(
        "Upload Documents",
        accept_multiple_files=True,
        type=["txt", "pdf", "docx"]
    )

    if uploaded_files:

        # Clear old files from the uploads directory
        for existing_file in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, existing_file)
            if os.path.isfile(file_path):
                os.remove(file_path)

        for file in uploaded_files:

            save_path = os.path.join(
                UPLOAD_DIR,
                file.name
            )

            with open(
                save_path,
                "wb"
            ) as f:
                f.write(file.getbuffer())

        st.success(
            f"{len(uploaded_files)} files uploaded."
        )

    if st.button(
        "Index Documents"
    ):

        count = index_documents(
            UPLOAD_DIR
        )
        
        st.session_state["chunks_indexed"] = count

        st.success(
            f"{count} chunks indexed."
        )



# -----------------------
# Search Tab
# -----------------------

with tab2:

    if st.session_state["chunks_indexed"] == 0:
        st.info("Please upload and index documents before you can search.")
    else:
        query = st.text_input(
            "Enter Search Query"
        )

        if st.button("Search"):

            if not query.strip():

                st.warning(
                    "Please enter a query."
                )

            else:

                results = semantic_search(
                    query
                )

                st.subheader(
                    "Top Results"
                )

                for match in results:

                    metadata = match.metadata

                    with st.expander(
                        f"Score: {match.score:.4f}"
                    ):

                        st.write(
                            f"**Source File:** {metadata.get('source_file')}"
                        )

                        st.write(
                            f"**Chunk Index:** {metadata.get('chunk_index')}"
                        )

                        st.write(
                            "**Retrieved Text:**"
                        )

                        st.write(
                            metadata.get("text")
                        )