from fastapi import APIRouter, UploadFile, File
import shutil
import os
import uuid
import json

from graph.workflow import build_graph

router = APIRouter()

graph = build_graph()

UPLOAD_DIR = "uploads"
MEMORY_FILE = "memory.json"

os.makedirs(UPLOAD_DIR, exist_ok=True)

# -------------------- MEMORY --------------------

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory_store = json.load(f)
else:
    memory_store = {}


def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_store, f)


# -------------------- ANALYZE --------------------

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
            "final_output": "",
            "question": "",
            "chat_answer": ""
        })

        # STORE FULL STATE
        memory_store[file_id] = result
        save_memory()

        return {
            "file_id": file_id,
            "output": result["final_output"]
        }

    except Exception as e:
        return {"error": str(e)}


# -------------------- CHAT --------------------

@router.post("/chat")
async def follow_up(data: dict):
    try:
        file_id = data.get("file_id")
        question = data.get("question")

        if file_id not in memory_store:
            return {"error": "Session not found"}

        previous_state = memory_store[file_id]

        result = graph.invoke({
            **previous_state,
            "question": question,
            "chat_answer": ""
        })

        # update memory
        memory_store[file_id] = result
        save_memory()

        return {"answer": result["chat_answer"]}

    except Exception as e:
        return {"error": str(e)}