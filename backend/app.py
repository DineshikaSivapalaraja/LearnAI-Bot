from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()

@app.get("/home")
async def welcome():
    return "Welcome to LearnAI Bot"

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    # Check file type --> pdf, document files allowed
    if not file.filename.endswith((".pdf", ".doc", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF or DOC files are allowed.")

    # save or process the file here
    content = await file.read()  

    return {
        "filename": file.filename,
        "type": file.content_type,
        "message": "File uploaded successfully"
    }


