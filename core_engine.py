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
    """
    print("🔍 Scanning for available models...")
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
    except Exception as e:
        print(f"⚠️ Could not list models: {e}")
        return 'gemini-1.5-flash'

    # Priority List
    priorities = [
        'gemini-1.5-flash', 
        'gemini-1.5-flash-latest', 
        'gemini-1.5-flash-001',
        'gemini-1.0-pro',
        'gemini-pro'
    ]

    for p in priorities:
        for available in available_models:
            if p in available:
                print(f"✅ Auto-Selected Model: {available}")
                return available
    
    if available_models:
        return available_models[0]
    
    return 'gemini-1.5-flash'

def clean_json_response(text):
    """
    Helper to strip markdown and ensure clean JSON string
    """
    clean_text = text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]
    return clean_text

def generate_quiz_from_pdf(file_path: str, num_questions: int = 5, topic: str = ""):
    print(f"--- Processing: {file_path} | Target: {num_questions} Questions | Topic: {topic} ---")
    
    # 1. Extract Text
    try:
        reader = PdfReader(file_path)
        text = ""
        # Read up to 20 pages to ensure we have enough content for 15+ questions
        for page in reader.pages[:20]:
            text += page.extract_text() + "\n"
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

    # 2. Setup AI
    model_name = get_best_model()
    model = genai.GenerativeModel(model_name)

    # 3. THE PAGINATION LOOP (The Fix)
    # We keep asking until we reach the target number
    all_questions = []
    attempts = 0
    max_attempts = 5  # Safety break
    
    while len(all_questions) < num_questions and attempts < max_attempts:
        needed = num_questions - len(all_questions)
        print(f"🔄 Batch {attempts+1}: Generating {needed} more questions...")

        topic_instruction = ""
        if topic and topic.strip() != "":
            topic_instruction = f"Focus on the topic: '{topic}'."

        prompt = f"""
        You are a teacher. Create {needed} multiple choice questions based on the text.
        
        CONTEXT:
        - We need a TOTAL of {num_questions} questions.
        - We currently have {len(all_questions)} questions.
        - You must generate exactly {needed} NEW questions now.
        - {topic_instruction}
        
        IMPORTANT:
        - Return ONLY valid JSON.
        - Do not repeat questions we already have.
        
        JSON Structure:
        {{
            "questions": [
                {{
                    "question": "Question text?",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "Correct Option",
                    "explanation": "Brief explanation"
                }}
            ]
        }}

        TEXT CONTENT:
        {text[:20000]} 
        """

        try:
            response = model.generate_content(prompt)
            clean_text = clean_json_response(response.text)
            data = json.loads(clean_text)
            
            batch = data.get("questions", [])
            
            # Add valid questions to our main list
            if batch:
                all_questions.extend(batch)
                print(f"✅ Got {len(batch)} questions. Total so far: {len(all_questions)}")
            else:
                print("⚠️ AI returned empty batch.")
                
            attempts += 1

        except Exception as e:
            print(f"⚠️ Error in batch generation: {e}")
            attempts += 1

    # 4. Final Polish
    # Trim list if we got too many (e.g. 16 instead of 15)
    final_questions = all_questions[:num_questions]
    
    print(f"🎉 Final Count: {len(final_questions)} Questions")

    return {
        "topic": topic if topic else "Generated Quiz",
        "questions": final_questions
    }

# --- TEST ---
if __name__ == "__main__":
    if os.path.exists("sample_notes.pdf"):
        result = generate_quiz_from_pdf("sample_notes.pdf", num_questions=15)
        if result:
            print(f"\n✅ SUCCESS! Generated {len(result['questions'])} questions.")
            for i, q in enumerate(result['questions']):
                print(f"{i+1}. {q['question']}")