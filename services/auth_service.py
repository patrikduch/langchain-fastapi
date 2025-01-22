from typing import Optional
from services.user_service import UserService

class AuthService:
    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[dict]:
        # Find the user by email
        user = UserService.users_collection.find_one({"email": email})
        if not user or user["password"] != password:  # Plain password comparison
            return None
        return {"id": str(user["_id"]), "name": user["name"], "email": user["email"]}