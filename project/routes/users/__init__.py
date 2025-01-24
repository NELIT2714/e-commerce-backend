from fastapi import APIRouter

from project import router_v1
from project.routes.users.dto import LoginUser, NewUser, UpdateUser

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/get/")
async def get_users_endpoint():
    pass


@users_router.get("/get/{user_id}/")
async def get_user_endpoint(user_id: int):
    pass


@users_router.post("/sign-up/")
async def user_signin_endpoint(user_data: NewUser):
    pass


@users_router.post("/sign-in/")
async def user_signin_endpoint(user_data: LoginUser):
    pass


@users_router.patch("/update/{user_id}/")
async def update_user_endpoint(user_id: int, admin_data: UpdateUser):
    pass


@users_router.delete("/delete/{user_id}/")
async def delete_user_endpoint(user_id: int):
    pass


router_v1.include_router(users_router)
