import os
from datetime import datetime
from pymongo import MongoClient
from pydantic import BaseModel, Field

# 1. Make a db file to connect mongo db
def get_mongo_collection():
    # Defaults to localhost, can be overridden by env var
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    db = client["cybersecurity_bot"]
    return db["chat_history"]

# 2. Make db schema for storing the prompts and answers
class ChatRecord(BaseModel):
    question: str
    answer: str
    context: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

def store_chat(question: str, answer: str, context: str):
    """Stores the chat interaction in MongoDB."""
    try:
        collection = get_mongo_collection()
        record = ChatRecord(question=question, answer=answer, context=context)
        # Using model_dump() as dict() is deprecated in Pydantic V2
        collection.insert_one(record.model_dump())
        print(f"✅ Chat stored in MongoDB: {record.timestamp}")
    except Exception as e:
        print(f"❌ Error storing chat in MongoDB: {e}")