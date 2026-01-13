# Cybersecurity Chatbot with MongoDB Logging

This project is a RAG-based chatbot that logs conversations to a MongoDB database.

## Setup Instructions

1.  **Install MongoDB**: Ensure MongoDB is installed and running locally on port 27017.
    *   [Download MongoDB Community Server](https://www.mongodb.com/try/download/community)

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ingest Data** (if not already done):
    ```bash
    python ingest.py
    ```

4.  **Start the Backend**:
    ```bash
    python chatbot.py
    ```

5.  **Start the Frontend** (in a new terminal):
    ```bash
    streamlit run frontend.py
    ```