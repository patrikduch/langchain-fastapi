from typing import List
from models.responses.user_response import UserResponse

users_db = []

class UserService:
    @staticmethod
    def get_all_users() -> List[UserResponse]:
        return users_db