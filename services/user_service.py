import logging
import os
from typing import List
from dotenv import load_dotenv
from fastapi import HTTPException
from pymongo import MongoClient
from models.requests.user_create_request import UserCreateRequest
from models.requests.user_register_request import UserRegisterRequest
from models.responses.user_response import UserResponse
from pymongo.errors import ConnectionFailure

load_dotenv()  # Load environment variables from .env file

# MongoDB Atlas connection
MONGO_URI = os.getenv("MONGO_URI")


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserService:

    # Initialize MongoDB client and database
    client = MongoClient(MONGO_URI)
    db = client["user"]  # Database name
    users_collection = db["user"]  # Collection name

    @staticmethod
    def check_database_connection() -> bool:
        try:
            # Perform a ping command using the MongoClient
            UserService.client.admin.command("ping")
            print("Database connection is successful.")
            return True
        except ConnectionFailure as e:
            print(f"Database connection failed: {e}")
            return False

    @staticmethod
    def get_all_users() -> List[UserResponse]:
        try:
            # Fetch all users from MongoDB
            user_documents = UserService.users_collection.find()


             # Convert MongoDB documents to UserResponse objects
            return [
                UserResponse(
                    id=str(user["_id"]),  # Convert ObjectId to string
                    username=user.get("name", ""),  # Use .get() to handle missing fields
                    email=user.get("email", "")  # Use .get() to handle missing fields
                )
                for user in user_documents
            ]
      

        except Exception as e:
            print(f"Error fetching users: {e}")
            return []  # Return an empty list in case of an error
    
    @staticmethod
    def create_user(user: UserCreateRequest) -> UserResponse:
        # Check for duplicate email
        existing_user = UserService.users_collection.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")

        # Insert new user
        new_user = user.dict()
        result = UserService.users_collection.insert_one(new_user)
        return UserResponse(
            id=str(result.inserted_id),
            name=new_user["name"],
            email=new_user["email"]
        )
    

    @staticmethod
    def register_user(user: UserRegisterRequest) -> dict:
        logger = logging.getLogger("register_user")
        try:
            logger.info(f"Attempting to register user with email: {user.email}")
            
            existing_user = UserService.users_collection.find_one({"email": user.email})
            if existing_user:
                logger.warning(f"Registration failed: Email {user.email} already exists")
                raise ValueError("Email already exists")
            
            user_data = {
                "name": user.username,
                "email": user.email,
                "password": user.password
            }
            result = UserService.users_collection.insert_one(user_data)
            
            logger.info(f"User registered successfully: {user.email}")
            return {"id": str(result.inserted_id), "name": user.username, "email": user.email}
        
        except ValueError as ve:
            logger.error(f"ValueError: {ve}")
            raise HTTPException(status_code=400, detail=str(ve))
        
        except Exception as e:
            logger.exception("An unexpected error occurred during registration")
            raise HTTPException(status_code=500, detail="An error occurred while registering the user")