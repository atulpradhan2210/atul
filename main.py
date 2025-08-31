# from typing import Annotated
# from typing_extensions import TypedDict
# from langgraph.graph import StateGraph, START, END
# from langgraph.graph.message import add_messages

# from dotenv import load_dotenv
# import os
# from langchain_google_genai import ChatGoogleGenerativeAI

# # Load API key
# load_dotenv()
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-pro",
#     api_key=os.getenv("GOOGLE_API_KEY")
# )

# # -------------------------------------------------------------------------
# # Define State
# class State(TypedDict):
#     messages: Annotated[list, add_messages()]

# # -------------------------------------------------------------------------
# # System instruction for medical AI
# SYSTEM_PROMPT = """
# You are Dr. MedAI, a highly knowledgeable and empathetic medical assistant.
# Your role:
# - Ask clarifying questions about patient symptoms.
# - Provide possible explanations and recommendations based on medical science.
# - Suggest next steps (tests, seeing a specialist, lifestyle advice).
# - Always include a disclaimer: "I am not a substitute for a licensed medical doctor. Please consult a professional before making health decisions."

# Style:
# - Clear
# - Compassionate
# - Evidence-based
# """

# # -------------------------------------------------------------------------
# # Node function (medical reasoning)
# def doctor_node(state: State):
#     messages = state["messages"]

#     # Ensure system prompt is always included
#     input_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

#     response = llm.invoke(input_messages)

#     # Append model reply to conversation state
#     return {"messages": response}

# # -------------------------------------------------------------------------
# # Build LangGraph workflow
# graph = StateGraph(State)
# graph.add_node("doctor", doctor_node)
# graph.add_edge(START, "doctor")
# graph.add_edge("doctor", END)
# medical_ai = graph.compile()

# # -------------------------------------------------------------------------
# # Example conversation
# response = medical_ai.invoke({"messages": [{"role": "user", "content": "I have a headache and fever. What could it be?"}]})

# # Print model's last response
# print(response["messages"][-1].content)

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os
# from langchain_google_genai import ChatGoogleGenerativeAI

# # Load env
# load_dotenv()
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# # Init LLM
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", api_key=GOOGLE_API_KEY)

# # FastAPI app
# app = FastAPI()

# # Allow frontend to talk to backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # 👈 change to your frontend domain in production
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Request body
# class ChatRequest(BaseModel):
#     message: str

# @app.post("/chat")
# def chat_endpoint(request: ChatRequest):
#     system_prompt = """
#     You are Dr. MedAI, a virtual medical assistant.
#     - Be empathetic, clear, and professional.
#     - Suggest possible causes and next steps.
#     - Always include this disclaimer: "This is not medical advice. Please consult a licensed doctor."
#     """

#     response = llm.invoke([
#         {"role": "system", "content": system_prompt},
#         {"role": "user", "content": request.message}
#     ])

#     return {"reply": response.content}


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", api_key=GOOGLE_API_KEY)

# FastAPI app
app = FastAPI()

# Allow frontend to talk to backend (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",              # Local React
        "https://frontend-owf2jhqch-atul-pradhans-projects-285a1070.vercel.app/",   # 👈 Replace with your Vercel frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body
class ChatRequest(BaseModel):
    message: str

# Root health check
@app.get("/")
def root():
    return {"status": "ok", "message": "Backend is running 🚀"}

# Chat endpoint
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
