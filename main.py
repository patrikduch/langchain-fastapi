import os
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.chat_models import ChatOpenAI

app = FastAPI()

load_dotenv()  # Load environment variables from .env file


# Initialize the ChatOpenAI model
model = ChatOpenAI(
    model_name="gpt-3.5-turbo",  # Specify the model
    temperature=0.8,            # Creativity level
    max_tokens=700,             # Response length
    verbose=True,                # Logs for debugging
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']

@app.get("/health")
async def checkHealth():

     # Example query
    query = "Give me 4 good books to read"

    # Get the response from the model
    response = await model.apredict(query)
    print("Response:", response)


    return {"message": "healthy"}


@app.get("/env")
async def env_variables():
    return {"DEBUG": DEBUG}