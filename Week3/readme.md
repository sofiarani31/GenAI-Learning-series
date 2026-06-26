# 📚 Semantic Search Engine

## Project Overview
This project is part of Week 3 of the GenAI Learning Series. It is a fully functional Semantic Search Engine designed to ingest unstructured company documents (PDFs, Word documents, Text files) and make them searchable using natural language queries. 

Unlike traditional keyword search (which only looks for exact word matches), this engine understands the *meaning* and *context* of a user's question, allowing it to retrieve relevant document sections even if the exact words don't match.

## 🧠 Core Learning Concepts

### 1. Text Embeddings
Embeddings are numerical representations of text. In this project, we use the open-source `sentence-transformers/all-MiniLM-L6-v2` model to convert sentences and paragraphs into dense 384-dimensional vectors. This allows the computer to mathematically map text based on its semantic meaning.

### 2. Semantic Similarity
Once text is converted into vectors, we can measure how closely related two pieces of text are by calculating the "distance" between their vectors. We use the **Cosine Similarity** metric. When a user asks a question, the system embeds the question and retrieves the document vectors that have the highest cosine similarity to the question vector.

### 3. Chunking Strategies
We cannot feed an entire 50-page employee handbook into an embedding model at once without losing precision. We implemented **Paragraph-Aware Chunking**. 
- The documents are split into logical paragraphs.
- Paragraphs are grouped together until they hit a maximum limit (e.g., `400 words`).
- To prevent breaking context across chunk boundaries, we use an **overlap** (e.g., `50 words`). 

### 4. Vector Databases (Pinecone)
Vector databases are specifically designed to store high-dimensional embeddings and execute lightning-fast similarity searches. In this project, we use **Pinecone Serverless** to store the document chunks alongside their metadata (like the source file name, chunk index, and the actual readable text).

## 🏗️ System Architecture

### 1. The Ingestion Pipeline (`src/index_documents.py`)
1. **Parser (`src/ingestion/parser.py`):** Reads raw `.txt`, `.pdf`, and `.docx` files.
2. **Cleaner (`src/ingestion/text_cleaner.py`):** Normalizes text (cleans spacing but preserves paragraph breaks).
3. **Chunker (`src/ingestion/chunker.py`):** Slices documents into paragraph-aware overlapping chunks.
4. **Embedder (`src/embeddings/embedding_model.py`):** Converts the chunks into 384-dimensional vectors.
5. **Database Client (`src/vectordb/pinecone_client.py`):** Upserts the vectors and the metadata into Pinecone.

### 2. The Retrieval Pipeline (`src/retrieval/search.py`)
1. Accepts a natural language query from the user.
2. Embeds the query using the exact same model used during ingestion.
3. Queries Pinecone for the `Top-K` nearest neighbors.
4. Returns the matched text, the similarity score, and the source file metadata to the user interface.

## 🛠️ Tech Stack
- **Language:** Python
- **UI:** Streamlit (`app.py`)
- **Embeddings:** `sentence-transformers`
- **Vector DB:** Pinecone
- **Document Parsing:** `pypdf`, `python-docx`

## 🚀 How to Run the Application

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Setup:**
   Ensure you have a `.env` file in the root directory with the necessary variables configured:
   ```env
   PINECONE_API_KEY=your_pinecone_api_key
   INDEX_NAME=company-docs
   EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
   CHUNK_SIZE=400
   CHUNK_OVERLAP=50
   TOP_K=3
   ```

3. **Start the Interface:**
   ```bash
   streamlit run app.py
   ```

4. **Usage:**
   - Navigate to the **Upload & Index** tab.
   - Upload your company documents and click "Index Documents".
   - Switch to the **Search** tab and type a natural language query to retrieve relevant document fragments!
