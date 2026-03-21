from fastapi import APIRouter, UploadFile, File
import shutil
import os
import uuid
import json

from graph.workflow import build_graph
from agents.chat_agent import chat_agent

router = APIRouter()

graph = build_graph()

UPLOAD_DIR = "uploads"
MEMORY_FILE = "memory.json"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# Load memory
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory_store = json.load(f)
else:
    memory_store = {}

def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_store, f)

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    try:
        if not file.content_type.startswith("image/"):
            return {"error": "Upload a valid image"}

        file_id = str(uuid.uuid4())
        file_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = graph.invoke({
            "image_path": file_path,
            "description": "",
            "structured": "",
            "reasoning": "",
            "final_output": ""
        })

        # store in memory
        memory_store[file_id] = {
            "description": result["description"],
            "structured": result["structured"],
            "reasoning": result["reasoning"],
            "final_output": result["final_output"]
        }

        save_memory()

        return {
            "file_id": file_id,
            "output": result["final_output"]
        }

    except Exception as e:
        return {"error": str(e)}


@router.post("/chat")
async def follow_up(data: dict):
    try:
        file_id = data.get("file_id")
        question = data.get("question")

        if file_id not in memory_store:
            return {"error": "Session not found"}

        context = memory_store[file_id]

        answer = chat_agent(question, context)

        return {"answer": answer}

    except Exception as e:
        return {"error": str(e)}