from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize LLM (will raise at call-time if key missing)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", api_key=GOOGLE_API_KEY)

app = FastAPI()

# ✅ CORS: NO trailing slash on origins
VERCEL_ORIGIN = "https://frontend-owf2jhqch-atul-pradhans-projects-285a1070.vercel.app"

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # local React dev
        VERCEL_ORIGIN,             # your Vercel frontend (no trailing slash)
    ],
    # (Optional) also allow any *.vercel.app if you change preview URLs often:
    # allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is running 🚀"}

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    system_prompt = """
    You are Dr. MedAI, a virtual medical assistant.
    - Be empathetic, clear, and professional.
    - Suggest possible causes and next steps.
    - Always include this disclaimer: "This is not medical advice. Please consult a licensed doctor."
    """
    response = llm.invoke([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": request.message}
    ])
    return {"reply": response.content}
