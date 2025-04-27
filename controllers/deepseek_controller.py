import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
import httpx
from models.prompt_request import PromptRequest

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

router = APIRouter()

@router.post("/")
async def deepseek_test(prompt_request: PromptRequest):
    async with httpx.AsyncClient(timeout=httpx.Timeout(30.0)) as client:
        response = await client.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
             "messages": [
                {"role": "system", "content": (
                    "You are DeepSeek, an AI assistant developed by DeepSeek. "
                    "Always respond politely and only in the Czech language. "
                    "If asked about your identity, always state that you are DeepSeek."
                )},
                {"role": "user", "content": prompt_request.prompt},
                ],
                "stream": False
            }
        )

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    data = response.json()

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise HTTPException(status_code=500, detail="Invalid response structure from DeepSeek API")

    print(content)
    return content
