from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

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

print("🔐 Cybersecurity Consultancy Bot Ready\n")

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break

    docs = db.similarity_search(question, k=3)
    context = "\n".join(d.page_content for d in docs)

    response = model.invoke(prompt.format(context=context, question=question))
    print("\nAI Helper:", response, "\n")
