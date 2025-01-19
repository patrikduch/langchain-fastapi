import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from controllers import langchain_controller

app = FastAPI()


# Allowed origins
origins = [
    "http://localhost",
    "https://localhost:3000", 
]


# Include routers from different controllers
app.include_router(langchain_controller.router, prefix="/langchain", tags=["LangChain"])


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow credentials like cookies
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']

@app.get("/health")
async def checkHealth():
    return {"message": "healthy"}


@app.get("/env")
async def env_variables():
    return {"DEBUG": DEBUG}