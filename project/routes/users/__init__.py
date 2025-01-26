from fastapi import APIRouter
from fastapi.responses import JSONResponse

from project import logger, router_v1
from project.database.crud.users import sign_up
from project.routes.users.dto import LoginUser, NewUser, UpdateUser

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/get/")
async def get_users_endpoint():
    pass


@users_router.get("/get/{user_id}/")
async def get_user_endpoint(user_id: int):
    pass


@users_router.post("/sign-up/")
async def user_signup_endpoint(user_data: NewUser):
    token = await sign_up(user_data.model_dump())
    return JSONResponse(status_code=200, content={"token": token})


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
