# Cybersecurity Consultancy Bot 🔐

A local RAG-based chatbot that acts as a cybersecurity consultant. It uses **Ollama (Llama 3)** for the LLM, **FAISS** for the vector store, **FastAPI** for the backend, and **Streamlit** for the frontend.

## 📋 Prerequisites

1.  **Python 3.10+** installed.
2.  **Ollama** installed and running.
    - Download from [ollama.com](https://ollama.com).
    - Pull the model:
      ```bash
      ollama pull llama3
      ```

## 🛠️ Installation

1.  Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-folder>
    ```

2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate.ps1 ( For Powershell )
    # Mac/Linux
    source venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 How to Run

You need to run the backend and frontend in **two separate terminals**.

### Terminal 1: Backend API
Start the FastAPI server.
```bash
python chatbot.py
```
*The server will start at `http://0.0.0.0:8000`.*

### Terminal 2: Frontend UI
Start the Streamlit interface.
```bash
streamlit run frontend.py
```
*The UI will open in your browser at `http://localhost:8501`.*

## 📂 Project Structure

- `chatbot.py`: The backend API server handling LLM logic.
- `frontend.py`: The Streamlit user interface.
- `vectorstore/`: The FAISS database containing the knowledge base.
- `requirements.txt`: List of dependencies.