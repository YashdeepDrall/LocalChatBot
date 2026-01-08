==========================
README: LocalChatBot
==========================

A local Python chatbot built in Python using Ollama for interactive Q&A.

Features:
- Run locally with Python
- Interactive chatbot session
- Lightweight and modular code
- Uses Ollama for AI responses
- Supports PDF and document processing (via PyPDF)
- Vector search using FAISS and sentence-transformers

Setup:
1. Clone the repository:
   git clone https://github.com/YashdeepDrall/LocalChatBot.git
   cd LocalChatBot

2. Create a Python virtual environment:
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate.ps1 (for PowerShell)
   # On Mac/Linux:
   source venv/bin/activate

3. Install Python dependencies:
   pip install -r requirements.txt

4. Prepare data embeddings:
   Run the data ingestion script to create vector embeddings:
   python ingest.py

5. Run the chatbot:
   python chatbot.py

Notes:
- Make sure Ollama is installed and configured locally.
- Some large dependencies (FAISS binaries, Sentence-Transformers models, Ollama models) are not in the repo.
  pip install -r requirements.txt will download necessary Python packages.
- Certain models or embeddings may download automatically on first run.
- Ensure you have internet access during first run to fetch models if needed.
- Always run ingest.py after adding new documents before using chatbot.py.

==========================
requirements.txt content
==========================

ollama
langchain
langchain-community
langchain-ollama
faiss-cpu
sentence-transformers
pypdf
python-dotenv
