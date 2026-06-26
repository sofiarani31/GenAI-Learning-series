# Week 3: Embeddings & Vector Databases

## Focus

This week focuses on representing unstructured text as numerical vectors using embedding models, preparing documents for retrieval, and storing searchable vectors in a vector database.

Key topics:

- Text embeddings
- Semantic similarity
- Document parsing
- Text cleaning and preprocessing
- Chunking strategies
- Chunk metadata design
- Vector database operations
- Top-k semantic retrieval
- Similarity scores
- Retrieval quality evaluation

## Weekly Project

### Semantic Search Engine over Document Corpus

Build a semantic search system that can process a folder of company documentation files and allow users to search the content using natural language queries.

The system should parse documentation files, split the content into meaningful chunks, generate embeddings for each chunk, store those embeddings in a vector database, and return the most relevant fragments for a user query.



## Project Goals

By the end of Week 3, the intern should be able to:

- Explain what embeddings are and why they are useful for semantic search.
- Convert text documents into searchable vector representations.
- Compare managed embedding APIs and open-source embedding models.
- Design chunking strategies that preserve useful context.
- Store vectors and metadata in a vector database.
- Query a vector database using embedded user queries.
- Return top-k relevant document fragments with similarity scores.
- Evaluate search quality using sample queries and expected results.
- Optionally use AWS Bedrock or an open-source embedding model for embedding generation.

## Functional Requirements

The application should:

- Accept a folder of company documentation files as input.
- Parse readable text from supported document formats.
- Clean and normalize extracted text where needed.
- Chunk documents into logical fragments.
- Generate embeddings for each chunk using either:
  - AWS Bedrock, or
  - an open-source embedding model such as `sentence-transformers/all-MiniLM-L6-v2`, `BAAI/bge-small-en-v1.5`, or `intfloat/e5-small-v2`
- Store chunk embeddings in a vector database.
- Store useful metadata with each chunk, such as source file, section title, chunk index, and character or token range where available.
- Accept a natural language search query from the user.
- Generate an embedding for the query using the same model used for the documents.
- Search the vector database for the top-k most similar chunks.
- Return relevant fragments with similarity scores and source metadata.
- Handle empty folders, unsupported files, failed parsing, and empty queries gracefully.

## Embedding Model Options

The intern may choose either a managed embedding service or an open-source embedding model.

Expected implementation practices:

- Keep the embedding model configurable.
- Use the same embedding model for both:
  - document chunks
  - user queries
- If using Amazon Bedrock, keep AWS configuration outside the codebase.
- If using an open-source model, document:
  - the model name
  - why it was selected
  - whether it runs locally or through Hugging Face / another hosted service
- Good beginner-friendly open-source choices:
  - `sentence-transformers/all-MiniLM-L6-v2`
  - `BAAI/bge-small-en-v1.5`
  - `intfloat/e5-small-v2`
- Keep model identifiers configurable.
- Read configuration from environment variables, credentials profiles, or application configuration.
- Avoid committing secrets, access keys, or private credentials.
- Log errors clearly without exposing sensitive information.




## Chunking Requirements

The intern should experiment with chunking strategies and document the final choice.

Beginner-friendly explanation:

- A chunk is a smaller piece of a large document.
- We create chunks because embedding models and vector search work better on focused pieces of text than on full long documents.
- If a chunk is too small, it may lose meaning.
- If a chunk is too large, retrieval becomes less precise.

Considerations:

- Chunk size
- Chunk overlap
- Section-aware splitting
- Paragraph-aware splitting
- Handling tables, lists, and headings
- Preserving source metadata
- Avoiding chunks that are too small to be meaningful
- Avoiding chunks that are too large to retrieve precisely

Recommended beginner strategy:

- Start with paragraph-aware chunking.
- Build chunks of around `300 to 500 words` or `500 to 800 tokens`.
- Use a chunk overlap of around `50 to 100 words` or `10 to 20%` of the chunk size.
- Keep headings with the paragraphs that follow them when possible.
- Store metadata for every chunk, such as source file, heading, chunk number, and text range.

What chunk overlap means:

- Overlap means repeating a small part of the previous chunk in the next chunk.
- This helps preserve context when an important sentence sits near a chunk boundary.
- Example:
  - Chunk 1 ends with a paragraph about password reset rules.
  - Chunk 2 starts by repeating the last few lines from Chunk 1, then continues with the next paragraph.
- Without overlap, retrieval may miss useful context.

At minimum, the project should include:

- One implemented chunking strategy
- The chosen chunk size
- The chosen overlap size
- Notes explaining why that strategy was selected

## Vector Database Requirements

The vector database should support:

- Inserting document chunk embeddings
- Storing metadata alongside vectors
- Querying by vector similarity
- Returning top-k matches
- Returning similarity or distance scores
- Rebuilding or refreshing the index when documents change

The implementation may use any suitable vector database, but the choice should be documented with a short explanation.

## Search Output Requirements

For each query, the system should return:

- User query
- Top-k matching fragments
- Similarity score for each result
- Source document name
- Relevant metadata, such as section title or chunk index
- The retrieved text fragment

The output should be readable enough for a user to understand why each result was returned.

## Deliverables

- Working semantic search application
- Document ingestion workflow
- Chunking implementation
- Embedding integration using AWS Bedrock or an open-source embedding model
- Vector database insertion and query workflow
- Sample company documentation corpus
- Sample queries and search results
- Notes explaining chunking decisions
- Notes explaining vector database choice
- Setup instructions for AWS configuration

## Evaluation Criteria

The project will be evaluated on:

- Correct document ingestion behavior
- Quality of chunking strategy
- Correct and consistent use of the selected embedding model
- Clean vector database integration
- Accuracy and usefulness of top-k search results
- Clear similarity score reporting
- Useful metadata in search results
- Graceful error handling
- Clear documentation
- Secure handling of AWS credentials and configuration

## Suggested Testing Scenarios

Test the system with:

- A short single-document corpus
- Multiple documents covering different topics
- Queries with exact keyword matches
- Queries that require semantic matching instead of exact keywords
- Empty query input
- Unsupported file types
- Re-indexing after adding new documents
- Different top-k values

## Recommended Learning Flow

1. Study embeddings and semantic similarity.
2. Review how text chunking affects retrieval quality.
3. Choose an embedding model:
   - AWS Bedrock, or
   - an open-source model
4. Parse a small sample documentation corpus.
5. Implement chunking and metadata generation.
6. Generate embeddings for document chunks.
7. Insert embeddings and metadata into a vector database.
8. Implement query embedding and top-k retrieval.
9. Test search quality with sample queries.
10. Document decisions, tradeoffs, and limitations.

## Stretch Goals

- Add a simple web interface for searching documents.
- Add filters by document name, department, or category.
- Add hybrid search using both keyword and vector search.
- Add automatic index refresh when files change.
- Add query result highlighting.
- Add an evaluation file with test queries and expected relevant documents.
- Add support for citations in search results.
- Add optional answer generation using retrieved fragments through AWS Bedrock or another LLM provider.
