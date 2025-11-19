import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from pypdf import PdfReader

# 1. Setup
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_best_model():
    """
    Automatically finds the best available model for your key.
    Prioritizes: Flash -> Pro -> 2.0 -> 1.5 -> 1.0
    """
    print("🔍 Scanning for available models...")
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
    except Exception as e:
        print(f"⚠️ Could not list models: {e}")
        # Fallback if listing fails
        return 'gemini-1.5-flash'

    # Priority List (The "Best" models to use)
    priorities = [
        'gemini-1.5-flash', 
        'gemini-1.5-flash-latest', 
        'gemini-1.5-flash-001',
        'gemini-1.0-pro',
        'gemini-pro'
    ]

    # Check if any priority model exists in your available list
    for p in priorities:
        # We check if the priority name is inside any available model name (e.g. "models/gemini-1.5-flash")
        for available in available_models:
            if p in available:
                print(f"✅ Auto-Selected Model: {available}")
                return available
    
    # If nothing matches, just take the first available one
    if available_models:
        print(f"⚠️ No preferred model found. Using: {available_models[0]}")
        return available_models[0]
    
    return 'gemini-1.5-flash' # Absolute fallback

def generate_quiz_from_pdf(file_path: str, num_questions: int = 5):
    print(f"--- Processing: {file_path} ---")
    
    # A. Read PDF (First 5 pages only to save speed)
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages[:5]:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

    # B. Get the Auto-Selected Model
    model_name = get_best_model()
    model = genai.GenerativeModel(model_name)

    # C. Prompt
    prompt = f"""
    You are a teacher. Create {num_questions} multiple choice questions from the text below.
    
    STRICT OUTPUT FORMAT:
    Return ONLY valid JSON. No markdown (```json). No text before or after.
    
    {{
        "topic": "Overall Topic",
        "questions": [
            {{
                "question": "Question text?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Correct Option Text",
                "explanation": "Brief explanation"
            }}
        ]
    }}

    TEXT:
    {text}
    """

    # D. Generate
    print(f"⏳ Generating with {model_name}...")
    try:
        response = model.generate_content(prompt)
        
        # Clean up JSON (Remove ```json if AI adds it)
        clean_text = response.text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
            
        return json.loads(clean_text)

    except Exception as e:
        print(f"❌ Generation Error: {e}")
        return None

# --- TEST ---
if __name__ == "__main__":
    if os.path.exists("sample_notes.pdf"):
        result = generate_quiz_from_pdf("sample_notes.pdf")
        if result:
            print(f"\n✅ SUCCESS! Topic: {result.get('topic', 'Unknown')}")
            print(f"   First Question: {result['questions'][0]['question']}")