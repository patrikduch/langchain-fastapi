from fastapi import APIRouter, HTTPException, Request

from models.requests.user_create_request import UserCreateRequest
from models.responses.user_response import UserResponse
from services.user_service import UserService

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
async def get_users():
    users = UserService.get_all_users()
    return users

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreateRequest):
    new_user = UserService.create_user(user)
    return new_user