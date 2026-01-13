from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from database import store_chat, update_chat_feedback
from analysis import analyze_response

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)

model = OllamaLLM(model="llama3")

template = """
You are a professional cybersecurity consultant.
Your job is to provide help and support related to cybersecurity consulting.

Rules:
- Answer ONLY from the provided context
- Be professional and practical
- If information is missing, say you need more data
- Do NOT guess or hallucinate

Context:
{context}

Client Question:
{question}

Consultant Answer:
"""

prompt = ChatPromptTemplate.from_template(template)


def get_context(question, k=3):
    docs = db.similarity_search(question, k=k)
    context = "\n".join(d.page_content for d in docs)
    return context, docs


def ask(question, k=3):
    context, docs = get_context(question, k=k)
    response = model.invoke(prompt.format(context=context, question=question))
    return response, context, docs


app = FastAPI(title="Cybersecurity Bot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str
    k: int = 3

class FeedbackRequest(BaseModel):
    chat_id: str
    feedback: str

@app.post("/feedback")
def feedback_endpoint(request: FeedbackRequest):
    update_chat_feedback(request.chat_id, request.feedback)
    return {"status": "success"}

@app.post("/ask")
def ask_endpoint(request: QueryRequest):
    response, context, docs = ask(request.question, k=request.k)
    
    # Analyze the response for specific criteria (apologies, unable to answer, etc.)
    flags = analyze_response(request.question, response)
    
    if flags:
        response += "\n\nFor further assistance, please contact support at iirissupport@gmail.com"
    
    # Store the conversation in MongoDB with flags
    chat_id = store_chat(request.question, response, context, flags=flags)
    
    serialized_docs = [{"page_content": d.page_content, "metadata": d.metadata} for d in docs]
    return {"answer": response, "context": context, "docs": serialized_docs, "chat_id": chat_id}

if __name__ == "__main__":
    print("Starting Backend Server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
