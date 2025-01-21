from fastapi import APIRouter, HTTPException, Request

from models.responses.user_response import UserResponse
from services.user_service import UserService

router = APIRouter()


@router.get("/", response_model=list[UserResponse])
async def get_users():
    users = UserService.get_all_users()
    return users