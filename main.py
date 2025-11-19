import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core_engine import generate_quiz_from_pdf

app = FastAPI(title="QuizGen AI")

# Allow external connections (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-quiz")
async def generate_quiz_endpoint(file: UploadFile = File(...), num_questions: int = 5):
    # 1. Validate PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # 2. Save file temporarily
    temp_filename = f"temp_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        # 3. Generate Quiz
        response = generate_quiz_from_pdf(temp_filename, num_questions)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # 4. Cleanup
        if os.path.exists(temp_filename):
            os.remove(temp_filename)