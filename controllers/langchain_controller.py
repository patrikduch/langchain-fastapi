import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from models.prompt_request import PromptRequest

router = APIRouter()

load_dotenv()  # Load environment variables from .env file

# Initialize the ChatOpenAI model
model = ChatOpenAI(

    model_name="chatgpt-4o-latest",  # Specify the model
    temperature=0.8,            # Creativity level
    max_tokens=700,             # Response length
    verbose=True,                # Logs for debugging
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

@router.post("/")
async def get_langchain(request: PromptRequest):
    try:
        # Get the prompt from the request body
        prompt = request.prompt

        # Get the response from the model
        response = await model.apredict(prompt)
        print("Response:", response)

        return {"response": response}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
    