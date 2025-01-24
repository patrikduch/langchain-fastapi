from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Request

from models.requests.user_create_request import UserCreateRequest
from models.requests.user_register_request import UserRegisterRequest
from models.responses.user_response import UserResponse
from security import validate_jwt
from services.user_service import UserService

router = APIRouter()

load_dotenv()  # Load environment variables from .env file

router.dependencies = [Depends(validate_jwt)]

# Protected endpoint
@router.get("/", response_model=list[UserResponse])
async def get_users():
    """
    Get all users. Only accessible to authenticated users.
    """
    # Optionally, you can check the user's role or permissions using the payload
    #if payload.get("role") != "admin":  # Example role-based check
    #    raise HTTPException(status_code=403, detail="Not enough permissions")

    # Fetch all users from the service
    users = UserService.get_all_users()
    return users

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreateRequest):
    new_user = UserService.create_user(user)
    return new_user


@router.post("/register")
async def register(user: UserRegisterRequest):
    try:
        new_user = UserService.register_user(user)
        return {"message": "User created successfully", "user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))