import requests
from ollama import Client
from fastapi import FastAPI, Response, HTTPException
from typing import Dict
import subprocess
import json

app = FastAPI()

OLLAMA_SERVER_URL = "http://ollama:11434"

ollama_client = Client(
    host=OLLAMA_SERVER_URL
)

def get_intent(user_input: str):
    messages = [{"role": "user", "content": user_input}]
    response = ollama_client.chat(
        model='ai-travel-agent', 
        messages=messages
    )
    
    message_content = response.get("message", {}).get("content", "")
    
    try:
        intent = json.loads(message_content)
        
        if isinstance(intent, dict) and "action" in intent:
            return intent
        else:
            return {"response": message_content}
    except json.JSONDecodeError:
        return {"response": message_content}

@app.post("/chat")
def chat(user_input: str):
    intent = get_intent(user_input)
    
    if not isinstance(intent, dict):
        return intent
    
    if intent.get("action") == "book":
        hotel = intent.get("hotel")
        check_in = intent.get("check_in")
        check_out = intent.get("check_out")
        adults = intent.get("adults")
        children = intent.get("children")
        
        if hotel and check_in and check_out and adults is not None and children is not None:
            return book_hotel(hotel, check_in, check_out, adults, children)
        else:
            raise HTTPException(status_code=400, detail="Missing booking details")
    
    elif intent.get("action") == "cancel":
        booking_id = intent.get("booking_id")
        if booking_id:
            return cancel_booking(booking_id)
        else:
            raise HTTPException(status_code=400, detail="Missing booking ID")
    
    elif intent.get("action") == "change_dates":
        booking_id = intent.get("booking_id")
        new_check_in = intent.get("new_check_in")
        new_check_out = intent.get("new_check_out")
        if booking_id and new_check_in and new_check_out:
            return change_booking(booking_id, new_check_in, new_check_out)
        else:
            raise HTTPException(status_code=400, detail="Missing details for date change")
    
    else:
        return intent

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