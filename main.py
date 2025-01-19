import os
from fastapi import FastAPI
from controllers import langchain_controller

app = FastAPI()


# Include routers from different controllers
app.include_router(langchain_controller.router, prefix="/langchain", tags=["LangChain"])


DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']

@app.get("/health")
async def checkHealth():
    return {"message": "healthy"}


@app.get("/env")
async def env_variables():
    return {"DEBUG": DEBUG}