from fastapi import FastAPI, UploadFile, File, HTTPException, Request
import os
from pydantic import BaseModel
# from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_community.embeddings.openai import OpenAIEmbeddings
# import openai

app = FastAPI()
# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

#store documents globally
documents = []
vector_store = None

@app.get("/home")
async def welcome():
    return "Welcome to LearnAI Bot"

# endpoint to upload and process a file
@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    
    #1. check file type --> pdf files allowed
    if not file.filename.endswith((".pdf")):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    #2. save file temporarily -> files stores in uploads directory
    content = await file.read()  
    file_path = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, "wb") as f:
        f.write(content)
        
    #3. load and split PDF text
    # Purpose: Extract text from the PDF and break it into smaller chunks
    # Why? AI models work better with smaller pieces of text, and this helps with searching and answering questions accurately
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    # split text into chunks of 1000 characters, with 200 characters overlap for context
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)
    documents.extend(split_docs)
    
    #4. create vector store (FAISS) for fast retrieval
    # Purpose: Convert text chunks into vectors (embeddings) so we can quickly find relevant parts of the document when a user asks a question
    # Why? This enables Retrieval-Augmented Generation (RAG), making Q&A much more accurate and efficient
    
    #open ai generations are not working due to rate limit error
    # embeddings = OpenAIEmbeddings()
    # global vector_Store
    # vector_Store = FAISS.from_documents(documents, embeddings)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    global vector_store
    vector_store = FAISS.from_documents(documents, embeddings)
    
    return {
        "filename": file.filename,
        "message": "File uploaded and processed successfully"
    }

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question")
    
    return {
        "question": question,
        "answer":"All is well!"
    }