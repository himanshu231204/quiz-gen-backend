# 🎓 QuizGen AI - Automated Study Assistant

![Project Status](https://img.shields.io/badge/Status-Live-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green)
![AI](https://img.shields.io/badge/AI-Google%20Gemini-orange)

**QuizGen AI** is a full-stack SaaS application that transforms passive study notes into active learning quizzes. Users can upload PDF course materials, specify a target topic, and instantly generate interactive Multiple Choice Questions (MCQs) with explanations.

🔗 **Live Demo:** [https://himanshu231204.github.io/quiz-gen-backend/](https://himanshu231204.github.io/quiz-gen-backend/)

---

## 🚀 Key Features

* **📄 PDF Analysis:** Instantly extracts text from uploaded course notes/syllabus.
* **🧠 Context-Aware AI:** Uses **Google Gemini 1.5 Flash** to generate relevant questions based on the specific PDF content.
* **🎯 Targeted Study:** Users can specify a "Topic" (e.g., *Dates*, *Formulas*, *Chapter 1*) to guide the quiz generation.
* **🔢 Dynamic Length:** Supports generating 3, 5, 10, or 15 questions dynamically using a smart pagination loop.
* **📥 PDF Export:** Users can download their generated quiz as a formatted PDF worksheet.
* **⚡ High Performance:** Hosted on a cloud-native architecture with keep-alive monitoring to prevent cold starts.

---

## 🛠️ Tech Stack

### **Backend (API)**
* **Framework:** Python (FastAPI)
* **AI Model:** Google Gemini 1.5 Flash (via Google GenAI SDK)
* **PDF Processing:** `pypdf`
* **Server:** Uvicorn
* **Hosting:** Render (Cloud)

### **Frontend (Client)**
* **Core:** HTML5, CSS3, Vanilla JavaScript
* **PDF Generation:** `html2pdf.js`
* **Hosting:** GitHub Pages

---

## ⚙️ Installation & Local Setup

If you want to run this project locally on your machine:

### 1. Clone the Repository
```bash
git clone [https://github.com/himanshu231204/quiz-gen-backend.git](https://github.com/himanshu231204/quiz-gen-backend.git)
cd quiz-gen-backend
````

### 2\. Create Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate
```

### 3\. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4\. Set Up Environment Variables

Create a `.env` file in the root folder and add your Google Gemini API Key:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 5\. Run the Server

```bash
uvicorn main:app --reload
```

The Backend API will start at `http://127.0.0.1:8000`.
You can then open `index.html` in your browser to test the Frontend.

-----

## 📂 API Documentation

Once the server is running, you can access the automatic Swagger UI documentation at:
👉 **[https://quiz-gen-backend-8h3k.onrender.com/docs](https://www.google.com/search?q=https://quiz-gen-backend-8h3k.onrender.com/docs)**

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Health check to verify server status. |
| `POST` | `/generate-quiz` | Uploads PDF and returns JSON quiz data. |

-----

## 🐛 Challenges & Solutions

**1. Serverless "Cold Start" Latency**

  * **Issue:** The free-tier Render server would "sleep" after 15 mins of inactivity, causing 60s+ delays.
  * **Solution:** Implemented a heartbeat monitor (UptimeRobot) to ping the health endpoint every 5 minutes, keeping the instance hot 24/7.

**2. AI Hallucinations (JSON Parsing)**

  * **Issue:** The LLM occasionally returned Markdown or conversational text instead of pure JSON.
  * **Solution:** Implemented a robust parsing loop that cleans markdown tags and retries generation if the JSON structure is invalid.

-----

## 👨‍💻 Author

**Himanshu Kumar**

  * **GitHub:** [himanshu231204](https://github.com/himanshu231204)
  * **Role:** Full Stack AI Engineer

-----

*Built with ❤️ using Python & Coffee.*

```

