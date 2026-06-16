# Week 4: Retrieval-Augmented Generation (RAG) Fundamentals

## Focus

This week focuses on combining retrieval and generation so an LLM can answer questions using uploaded documents instead of relying only on its own pre-trained knowledge.

Key topics:

- Retrieval-Augmented Generation (RAG)
- PDF ingestion and text extraction
- Chunk retrieval for question answering
- Prompt grounding with retrieved context
- Source citation in responses
- Multi-document chat workflows
- Reducing hallucinations

## Weekly Project

### Chat with Your PDF Knowledge Base Application

Build a web-based application using **Streamlit** or **Chainlit** where a user can:

- Upload one or more PDF documents
- Index the documents for retrieval
- Ask questions in a chat interface
- Receive grounded answers based on the uploaded files
- View the source chunks used to generate each answer

## What Needs to Be Done

- Build a PDF upload flow
- Extract text from uploaded PDFs
- Split documents into meaningful chunks
- Generate embeddings for those chunks
- Store chunk embeddings in a vector database
- Retrieve the most relevant chunks for each user question
- Send the retrieved context to the LLM with the user query
- Return a final answer in chat format
- Show source references for every answer
- Handle empty uploads, invalid PDFs, and missing results gracefully

## Functional Expectations

The application should:

- Support multiple PDF uploads
- Reuse the retrieval pipeline from the previous semantic search project where possible
- Use the same embedding model for indexing and querying
- Return concise answers grounded in retrieved content
- Show the document name and relevant text snippet as references
- Keep the chat history visible during the session

## Suggested Folder Structure

```text
week4-rag-project/
├── app.py
├── requirements.txt
├── uploads/
├── data/
│   └── processed/
├── src/
│   ├── config.py
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── prompt_builder.py
│   ├── rag_chain.py
│   └── utils.py
├── tests/
└── README.md
```

## Deliverables

- Working RAG-based chat application
- PDF upload and processing workflow
- Retrieval pipeline connected to an LLM
- Source-aware answers in the chat UI
- Clear setup and run instructions

## Suggested Flow

1. Upload PDFs
2. Extract and clean text
3. Chunk the content
4. Create embeddings and store them
5. Retrieve top matching chunks for a question
6. Pass the retrieved context to the LLM
7. Return the answer with source references

## Stretch Ideas

- Add conversation memory
- Support citations with page numbers
- Allow filtering by selected document
- Add re-indexing when new PDFs are uploaded
