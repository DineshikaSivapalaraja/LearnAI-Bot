from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline, AutoTokenizer

load_dotenv()
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   #"http://localhost:5173"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#store documents globally
vector_store = None
documents = []

# request schema
class QuestionRequest(BaseModel):
    question: str

@app.get("/home")
async def welcome():
    return {"message": "Welcome to LearnAI Bot"}

# endpoint to upload and process a file
@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    
    #1. check file type --> pdf files allowed
    if not file.filename.endswith(".pdf"):
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

    # load embeddings for vector store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    global vector_store
    vector_store = FAISS.from_documents(documents, embeddings)

    return {
        "filename": file.filename,
        "message": "File uploaded and processed successfully"
    }

# endpoint to ask question and retrieve answer from pretrained model
@app.post("/ask")
async def ask_question(req: QuestionRequest):
    
    #1. validate document is available
    if not vector_store:
        raise HTTPException(status_code=400, detail="No documents uploaded yet. Please upload a PDF first.")
    
    #2. load local text generation model to answer questions
    # Purpose: Initialize the AI model that will generate natural language answers
    # Why? Need a language model to understand context and generate human-like responses
    model_name =  "google/flan-t5-small"  #  "google/flan-t5-base" , "distilgpt2" also possible
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    generator = pipeline(
        "text2text-generation",   # flan-t5-small is not use text-generation
        model=model_name,
        tokenizer=tokenizer
    )

    #3. retrieve relevant document chunks based on the question
    # Purpose: Find the most relevant parts of the uploaded PDF that relate to the user's question
    # Why? Instead of sending the entire document to the AI (which would be slow and confusing), 
    # we only send the most relevant chunks that likely contain the answer
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})  # fetch top 3 most similar chunks(optional)
    relevant_docs = retriever.get_relevant_documents(req.question)
    
    #4. combine retrieved chunks into context
    # Purpose: Create a single text block containing all relevant information
    # Why? The AI model needs context in a readable format to generate accurate answers
    context = "\n".join(doc.page_content for doc in relevant_docs)

    #5. create a structured prompt for the AI model
    # Purpose: Give the AI clear instructions and context to generate a good answer
    # Format: Instructions + Context + Question --> for better AI response
    
    prompt = f"""
Hello!, You are an AI assistant. Use the following context to answer the user's question concisely and clearly.

Context:
{context}

Question: {req.question}
""".strip()

    #6. generate the answer using the AI model
    # Purpose: Use the language model to create a natural language response based on the context
    # Why? This is the core of RAG (Retrieval-Augmented Generation) - we retrieve relevant info, 
    #  then generate an answer based on that specific information
    response = generator(prompt, max_length=256, do_sample=False)
    answer = response[0]['generated_text'].strip()

    return {
        "question": req.question,
        "answer": answer
    }


