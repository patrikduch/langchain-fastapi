import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from openai import OpenAI

from models.prompt_request import PromptRequest
from security import validate_jwt

client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

router = APIRouter()

#router.dependencies = [Depends(validate_jwt)]


load_dotenv()  # Load environment variables from .env file


@router.post("/")
async def deepseek_test(prompt_request: PromptRequest):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt_request.prompt},
        ],
        stream=False
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content