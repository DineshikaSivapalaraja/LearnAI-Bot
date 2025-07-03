# LearnAI-Bot

## Backend

Q&A chatbot that allows users to upload PDF file and ask questions about their content using AI-powered retrieval-augmented generation (RAG).

### Technologies

- **FastAPI** - High-performance web framework for building REST APIs
- **LangChain** - Framework for developing applications with language models and RAG pipelines
- **Hugging Face** - Pre-trained AI models for embeddings and text generation
  - `google/flan-t5-small` or `google/flan-t5-base` - Text-to-text generation model for Q&A
  - `sentence-transformers/all-MiniLM-L6-v2` - Embedding model for semantic search
- **Transformers** - Library for loading and using pre-trained language models
- **FAISS** - Vector database for fast similarity search and retrieval

### Architecture

The application follows a RAG (Retrieval-Augmented Generation) pattern:

1. **Document Processing**: PDFs are uploaded, text extracted, and split into chunks
2. **Embedding Creation**: Text chunks are converted to vector embeddings
3. **Vector Storage**: Embeddings stored in FAISS for fast similarity search
4. **Question Processing**: User questions are embedded and matched against document chunks
5. **Answer Generation**: Relevant chunks provide context for AI model to generate accurate answers

### Work flow of API Endpoints

#### 1. Welcome Message
```
GET /home
```
Returns a welcome message to verify the API is running.

#### 2. Upload PDF Document
```
POST /upload-file
```
- **Input**: PDF file (form-data)
- **Process**: Extracts text, creates chunks, generates embeddings, builds vector store
- **Output**: Success confirmation with filename

#### 3. Ask Questions
```
POST /ask
```
- **Input**: JSON with question field
- **Process**: Retrieves relevant chunks, generates AI response using T5 model
- **Output**: Question and AI-generated answer

### Backend Setup

1) .venv\Scripts\activate  --> (windows)

2) cd backend

3) pip install -r requirements.txt

4) Setup env variables in .env as .env.example

### Run the Backend Server
```
uvicorn app:app --reload
```

## Frontend

React based responsive web interface with clean UI for document upload and AI-powered Q&A interaction.

### Frontend Setup

1) cd frontend
2) npm install
3) Setup env variables as .env.example

### Run the Frontend

```
npm run dev
```
