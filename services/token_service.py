from datetime import datetime, timedelta
import os
from typing import Optional
from dotenv import load_dotenv
from jose import JWTError, jwt
from fastapi import HTTPException, status

load_dotenv()  # Load environment variables from .env file

ACCESS_TOKEN_EXPIRE_MINUTES = 30

class TokenService:
    @staticmethod
    def create_access_token(data: dict) -> str:
        """
        Create a JWT access token with the given data.

        :param data: Dictionary containing the data to encode in the token
        :return: Encoded JWT token
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> Optional[dict]:
        """
        Decode and validate a JWT access token.

        :param token: The JWT token to decode
        :return: Decoded token data if valid, raises an exception if invalid
        """
        try:
            payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
            return payload
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from e
