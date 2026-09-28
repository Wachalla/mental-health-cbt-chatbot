# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
from thought_record_bot_final import ThoughtRecordBot
import uvicorn

# --- Application Setup ---
app = FastAPI(
    title="Mental Health CBT Chatbot API",
    description="An API to interact with the T-Bot for guided CBT exercises.",
    version="1.0.0"
)

# In a real application, you'd manage user sessions more robustly (e.g., with a database)
# For this example, we'll store active sessions in a simple dictionary.
active_sessions = {}

# --- API Data Models ---
class UserInput(BaseModel):
    user_id: str
    message: str

class BotResponse(BaseModel):
    user_id: str
    response: str

# --- API Endpoints ---
@app.post("/chat", response_model=BotResponse)
def chat_with_bot(user_input: UserInput):
    """
    Main endpoint to send a message to the chatbot and get a response.
    """
    user_id = user_input.user_id
    message = user_input.message

    # Get the user's session or create a new one
    if user_id not in active_sessions:
        print(f"Creating new session for user: {user_id}")
        active_sessions[user_id] = ThoughtRecordBot(user_id=user_id)
    
    bot_instance = active_sessions[user_id]
    
    # Get the response from the bot's logic
    response_text = bot_instance.get_response(message)
    
    return BotResponse(user_id=user_id, response=response_text)

@app.get("/")
def read_root():
    return {"status": "Mental Health Chatbot API is running."}

# This part allows running the app directly for testing
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
