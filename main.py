import logging
import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from controllers import auth_controller, langchain_controller, user_controller
from slowapi.errors import RateLimitExceeded
from limiter import limiter

# Configure Logging
logging.basicConfig(
    level=logging.INFO,  # Set the desired log level (INFO or DEBUG)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

logger.info('API is starting up')

# Allowed origins
origins = [
    "http://localhost",
    "https://localhost:3000",
    "https://assistifyai-fe-h2aveuccbsc2hfc0.westeurope-01.azurewebsites.net",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow credentials like cookies
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    logger.warning(f"Rate limit exceeded for {request.url}: {exc}")
    return PlainTextResponse(str(exc), status_code=429)

# Include routers from different controllers
app.include_router(auth_controller.router, prefix="/auth", tags=["Auth"])
app.include_router(langchain_controller.router, prefix="/langchain", tags=["LangChain"])
app.include_router(user_controller.router, prefix="/users", tags=["Users"])


DEBUG = os.getenv('DEBUG', 'False').lower() in ['true', '1', 't']
logger.info(f"DEBUG environment variable is set to: {DEBUG}")

# Attach the limiter to the app
app.state.limiter = limiter

# Log requests middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

@app.get("/health")
async def checkHealth():
    logger.info("Health check endpoint was accessed.")
    return {"message": "healthy"}
