from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env and API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- App Setup ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-Memory Chat History ---
chat_history = []

# --- Models ---
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

# --- Endpoint ---
@app.post("/chat", response_model=QueryResponse)
async def chat_endpoint(req: QueryRequest):
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a multilingual AI assistant. Match your reply language and script to the user's input:\n"
                        "- If user types in English, reply in English.\n"
                        "- If user types Hindi using English letters, reply in Roman Hindi.\n"
                        "- If user types Hindi in Devanagari, reply in Devanagari.\n"
                        "Mirror the user’s language and do not translate unless asked."
                    )
                },
                {"role": "user", "content": req.query}
            ]
        )

        reply = completion.choices[0].message.content.strip()

        # Save to history
        chat_history.append({
            "question": req.query,
            "answer": reply
        })

        return {"response": reply}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
