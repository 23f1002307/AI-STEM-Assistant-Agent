from fastapi import APIRouter, UploadFile, File
import shutil
import os
from graph.workflow import build_graph

router = APIRouter()

graph = build_graph()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = graph.invoke({
        "image_path": file_path
    })

    return {"output": result["final_output"]}