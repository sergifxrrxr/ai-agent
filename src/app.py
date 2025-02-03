import redis
import requests
from ollama import Client
from fastapi import FastAPI, Response, HTTPException, Depends
from typing import Dict, List
import subprocess
import json
import uuid
from init_db import init_db

app = FastAPI()

init_db()

redis_client = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)

OLLAMA_SERVER_URL = "http://ollama:11434"
ollama_client = Client(host=OLLAMA_SERVER_URL)

SESSION_EXPIRY = 3600

def get_session_id(session_id: str = None):
    if session_id is None:
        session_id = str(uuid.uuid4())
    return session_id

def save_message_to_session(session_id: str, role: str, content: str):
    key = f"chat_session:{session_id}"
    message = json.dumps({"role": role, "content": content})
    redis_client.rpush(key, message)
    redis_client.expire(key, SESSION_EXPIRY)

def get_chat_history(session_id: str) -> List[Dict[str, str]]:
    key = f"chat_session:{session_id}"
    messages = redis_client.lrange(key, 0, -1)
    return [json.loads(msg) for msg in messages] if messages else []

def get_intent(user_input: str, session_id: str):    
    history = get_chat_history(session_id)
    
    save_message_to_session(session_id, "user", user_input)
    
    history.append({"role": "user", "content": user_input})

    response = ollama_client.chat(
        model='ai-travel-agent',
        messages=history
    )

    message_content = response.get("message", {}).get("content", "")
    
    try:
        intent = json.loads(message_content)
        
        save_message_to_session(session_id, "assistant", message_content)

        if isinstance(intent, dict) and "action" in intent:
            return intent
        else:
            return {"response": message_content}
    except json.JSONDecodeError:
        save_message_to_session(session_id, "assistant", message_content)
        return {"response": message_content}

@app.post("/chat")
def chat(user_input: str, session_id: str = None):
    session_id = get_session_id(session_id)
    intent = get_intent(user_input, session_id)

    if not isinstance(intent, dict):
        return {"session_id": session_id, **intent}

    if intent.get("action") == "book":
        hotel = intent.get("hotel")
        check_in = intent.get("check_in")
        check_out = intent.get("check_out")
        adults = intent.get("adults")
        children = intent.get("children")

        if hotel and check_in and check_out and adults is not None and children is not None:
            return {"session_id": session_id, **book_hotel(hotel, check_in, check_out, adults, children)}

    elif intent.get("action") == "cancel":
        booking_id = intent.get("booking_id")
        if booking_id:
            return {"session_id": session_id, **cancel_booking(booking_id)}

    elif intent.get("action") == "change_dates":
        booking_id = intent.get("booking_id")
        new_check_in = intent.get("new_check_in")
        new_check_out = intent.get("new_check_out")
        if booking_id and new_check_in and new_check_out:
            return {"session_id": session_id, **change_booking(booking_id, new_check_in, new_check_out)}

    return {"session_id": session_id, **intent}

def book_hotel(hotel: str, check_in: str, check_out: str, adults: int, children: int):
    try:
        result = subprocess.run([
            "python", "book_hotel.py", hotel, check_in, check_out, str(adults), str(children)
        ], capture_output=True, text=True)

        if result.returncode == 0:
            return {"status": "OK", "message": result.stdout.strip()}
        else:
            raise HTTPException(status_code=400, detail=result.stderr.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def cancel_booking(booking_id: str):
    try:
        result = subprocess.run(["python", "cancel_booking.py", booking_id], capture_output=True, text=True)

        if result.returncode == 0:
            return {"status": "OK", "message": result.stdout.strip()}
        else:
            raise HTTPException(status_code=400, detail=result.stderr.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def change_booking(booking_id: str, new_check_in: str, new_check_out: str):
    try:
        result = subprocess.run(["python", "change_dates.py", booking_id, new_check_in, new_check_out], capture_output=True, text=True)

        if result.returncode == 0:
            return {"status": "OK", "message": result.stdout.strip()}
        else:
            raise HTTPException(status_code=400, detail=result.stderr.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)