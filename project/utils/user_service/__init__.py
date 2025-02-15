from typing import TYPE_CHECKING, Optional, Union
from fastapi import HTTPException
from project.schemas.user import UserOut

if TYPE_CHECKING:
    from project.database.crud import UserRepository

class UserService:
    def __init__(self, user_repository: "UserRepository"):
        self.user_repository = user_repository

    async def get_user(self, user_id: int = None, username: str = None, email: str = None) -> Union[UserOut, HTTPException]:
        user = await self.user_repository.get_user(user_id=user_id, username=username, email=email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    async def create_user(self, user_data: dict) -> str:
        token = await self.user_repository.create_user(user_data=user_data)
        return token
    
    async def update_account(self, user_id: int, account_data: dict) -> Optional[HTTPException]:
        return await self.user_repository.update_account(user_id=user_id, account_data=account_data)
    
    async def update_personal_data(self, user_id: int, personal_data: dict) -> Optional[HTTPException]:
        return await self.user_repository.update_personal_data(user_id=user_id, personal_data=personal_data)
    
    async def update_delivery_data(self, user_id: int, delivery_data: dict) -> Optional[HTTPException]:
        return await self.user_repository.update_personal_data(user_id=user_id, delivery_data=delivery_data)

    async def login(self, user_data: dict) -> str:
        token = await self.user_repository.login(user_data=user_data)
        return token
    
    async def logout(self, token: str) -> Optional[HTTPException]:
        return await self.user_repository.logout(token=token)
