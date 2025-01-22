from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from models.requests.user_login_request import UserLoginRequest
from models.requests.user_register_request import UserRegisterRequest
from models.responses.token_response import TokenResponse
from services.token_service import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from services.user_service import UserService
from fastapi import HTTPException, Depends


router = APIRouter()

@router.post("/auth/login", response_model=TokenResponse)
async def login(login_request: UserLoginRequest):
    # Fetch user from MongoDB
    user = UserService.users_collection.find_one({"email": login_request.email})

    # Check if user exists and password matches
    if not user or user["password"] != login_request.password:  # Plaintext password comparison
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT Token
    access_token = jwt.encode(
        {"sub": user["email"], "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}