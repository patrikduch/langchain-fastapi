import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from langchain.chat_models import ChatOpenAI
from models.prompt_request import PromptRequest
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

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
    

@router.post("/code-prompt")
async def get_langchain_code_prompt():
    try:

        code_prompt = PromptTemplate(
            template="Write a very short {language} function that will {task}",
            input_variables=["language", "task"]
        )

        code_chain = LLMChain(
            llm=model,
            prompt=code_prompt
        )

        result = code_chain({
            "language": "python",
            "task": "return a list of numbers"
        })

        return {"response": result["text"]}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="An error occurred while processing the request.")
    
    