import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

documents = []

for file in os.listdir("data"):
    path = os.path.join("data", file)

    if file.endswith(".txt"):
        documents.extend(
            TextLoader(path, encoding="utf-8", autodetect_encoding=True).load()
        )

    elif file.endswith(".pdf"):
        documents.extend(PyPDFLoader(path).load())

if not documents:
    raise ValueError("❌ No documents loaded")

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.from_documents(chunks, embeddings)
db.save_local("vectorstore")

print("✅ Knowledge base created successfully")
