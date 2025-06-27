from fastapi import FastAPI, UploadFile, File, HTTPException, Request
import os

app = FastAPI()

@app.get("/home")
async def welcome():
    return "Welcome to LearnAI Bot"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Check file type --> pdf, document files allowed
    if not file.filename.endswith((".pdf", ".doc", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF or DOC files are allowed.")

    content = await file.read()  
    
    # Save file to disk
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as f:
        f.write(content)

    return {
        "filename": file.filename,
        "type": file.content_type,
        "message": "File uploaded successfully"
    }

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question")
    
    return {
        "question": question,
        "answer":"All is well!"
    }