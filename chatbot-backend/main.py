from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import openai
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow CORS for frontend interaction (optional)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = os.getenv("OPENAI_API_KEY")

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_request: ChatRequest):
    if not openai.api_key:
        raise HTTPException(status_code=500, detail="OpenAI API key not configured.")
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": chat_request.message}
            ],
            max_tokens=500,
            temperature=0.7,
        )
        answer = completion.choices[0].message.content.strip()
        return ChatResponse(response=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
