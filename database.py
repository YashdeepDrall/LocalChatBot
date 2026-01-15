import os
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

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
    flags: List[str] = []
    user_feedback: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

def store_chat(question: str, answer: str, context: str, flags: Optional[List[str]] = None) -> str:
    """Stores the chat interaction in MongoDB."""
    try:
        if flags is None:
            flags = []
        collection = get_mongo_collection()
        record = ChatRecord(question=question, answer=answer, context=context, flags=flags)
        # Using model_dump() as dict() is deprecated in Pydantic V2
        result = collection.insert_one(record.model_dump())
        print(f"✅ Chat stored in MongoDB: {record.timestamp}")
        return str(result.inserted_id)
    except Exception as e:
        print(f"❌ Error storing chat in MongoDB: {e}")
        return ""

def update_chat_feedback(chat_id: str, feedback: str):
    """Updates the chat record with user feedback."""
    try:
        collection = get_mongo_collection()
        collection.update_one({"_id": ObjectId(chat_id)}, {"$set": {"user_feedback": feedback}})
        print(f"✅ Feedback updated for {chat_id}: {feedback}")
    except Exception as e:
        print(f"❌ Error updating feedback: {e}")
