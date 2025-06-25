from fastapi import FastAPI 

app = FastAPI()

@app.get("/home")
async def welcome():
    return "Welcome to LearnAI Bot"