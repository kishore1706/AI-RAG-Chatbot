from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_project_openrouter import RAGProject
from blob_storage import download_blob, blob_exists
import os

app = FastAPI(title="RAG Chatbot API")

# Allow React frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

PDF_FOLDER = "data"

os.makedirs(PDF_FOLDER, exist_ok=True)

files = [
    "5. Battery Management Systems.pdf",
    "Sensor Fusion for ADAS.pdf",
    "faiss_openrouter_index.idx",
    "faiss_openrouter_docs.pkl",
]

for file in files:
    destination = os.path.join(PDF_FOLDER, file)

    if not os.path.exists(destination):
        if blob_exists(file):
            download_blob(file, destination)

rag = RAGProject(PDF_FOLDER)
rag.index_path = os.path.join(PDF_FOLDER, "faiss_openrouter_index.idx")
rag.docs_path = os.path.join(PDF_FOLDER, "faiss_openrouter_docs.pkl")

rag.load_index()

class ChatRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "RAG Backend Running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat")
def chat(request: ChatRequest):

    answer = rag.ask(request.question)

    return {
        "answer": answer
    }