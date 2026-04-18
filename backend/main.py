from fastapi import FastAPI
from pydantic import BaseModel
from agent import graph
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base
from models import Interaction


app = FastAPI()

Base.metadata.create_all(bind=engine)

# 🔥 CORS FIX (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatInput(BaseModel):
    message: str

@app.get("/")
def home():
    return {"message": "AI CRM Backend Running"}

@app.post("/chat")
def chat(data: ChatInput):
    result = graph.invoke({"input": data.message})

    return {
        "response": result.get("output", ""),
        "extracted": result.get("extracted"),
        "updated": result.get("updated")   # ✅ ADD THIS
    }

@app.get("/clear")
def clear_db():
    db = SessionLocal()
    db.query(Interaction).delete()
    db.commit()
    db.close()
    return {"message": "Database cleared"}