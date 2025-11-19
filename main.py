import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from core_engine import generate_quiz_from_pdf

app = FastAPI(title="QuizGen AI")

# --- CRITICAL SECURITY FIX (CORS) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all websites (GitHub Pages, localhost, etc.)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (POST, GET, etc.)
    allow_headers=["*"],  # Allow all headers
)
# ------------------------------------

@app.get("/")
def home():
    return {"message": "QuizGen AI is Live! 🚀"}

@app.post("/generate-quiz")
async def generate_quiz_endpoint(
    file: UploadFile = File(...), 
    num_questions: int = Form(5), 
    topic: str = Form("")
):
    # 1. Validate PDF
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # 2. Save file temporarily
    temp_filename = f"temp_{file.filename}"
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # 3. Generate Quiz
        response = generate_quiz_from_pdf(temp_filename, num_questions, topic)
        return response

    except Exception as e:
        print(f"❌ Server Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
        
    finally:
        # 4. Cleanup
        if os.path.exists(temp_filename):
            os.remove(temp_filename)