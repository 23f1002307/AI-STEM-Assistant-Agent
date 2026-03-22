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

# ---------------- MEMORY ----------------

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory_store = json.load(f)
else:
    memory_store = {}


def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory_store, f)


# ---------------- STEP 1: ANALYZE ----------------

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
            "chat_answer": "",
            "user_decision": ""
        })

        memory_store[file_id] = result
        save_memory()

        return {
            "file_id": file_id,
            "preview": result["description"],
            "message": "Confirm / Reject / Skip to continue"
        }

    except Exception as e:
        return {"error": str(e)}


# ---------------- STEP 2: USER DECISION ----------------

@router.post("/decision")
async def user_decision(data: dict):
    try:
        file_id = data.get("file_id")
        decision = data.get("decision")

        if file_id not in memory_store:
            return {"error": "Session not found"}

        state = memory_store[file_id]

        # 🔥 REJECT → re-run vision
        if decision == "reject":
            result = graph.invoke({
                **state,
                "user_decision": "reject"
            })

            memory_store[file_id] = result
            save_memory()

            return {
                "type": "preview",
                "preview": result["description"],
                "message": "Reprocessing the image. Please review again."
            }

        # 🔥 CONFIRM / SKIP → continue pipeline
        result = graph.invoke({
            **state,
            "user_decision": decision
        })

        memory_store[file_id] = result
        save_memory()

        return {
            "type": "final",
            "output": result["final_output"]
        }

    except Exception as e:
        return {"error": str(e)}

# ---------------- CHAT ----------------

@router.post("/chat")
async def follow_up(data: dict):
    try:
        file_id = data.get("file_id")
        question = data.get("question")

        if file_id not in memory_store:
            return {"error": "Session not found"}

        state = memory_store[file_id]

        result = graph.invoke({
            **state,
            "question": question
        })

        return {"answer": result["chat_answer"]}

    except Exception as e:
        return {"error": str(e)}