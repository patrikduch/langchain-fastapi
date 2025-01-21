import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse  
from controllers import langchain_controller

from slowapi.errors import RateLimitExceeded

from limiter import limiter

app = FastAPI()


# Allowed origins
origins = [
    "http://localhost",
    "https://localhost:3000",
    "https://assistifyai-fe-h2aveuccbsc2hfc0.westeurope-01.azurewebsites.net", 
]

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return PlainTextResponse(str(exc), status_code=429)


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


# Attach the limiter to the app
app.state.limiter = limiter


@app.get("/health")
async def checkHealth():
    return {"message": "healthy"}


@app.get("/env")
@limiter.limit("5/minute")
async def env_variables(request: Request):
    return {"DEBUG": DEBUG}