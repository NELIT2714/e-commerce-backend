from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from project import router_v1
from project.database.mariadb import get_db
from project.functions import verify_token
from project.routes.users.dto import LoginUser, NewUser, UpdateUser, PersonalData, DeliveryData
from project.schemas.user import UserOut
from sqlalchemy.ext.asyncio import AsyncSession

from project.utils import SessionDBManager, UserService

from project.database.crud import UserRepository

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/get/me/", response_model=UserOut)
async def get_user_endpoint(result_token: str = Depends(verify_token)):
    user_service = UserService(UserRepository(SessionDBManager()))
    user = await user_service.get_user(user_id=result_token.data["token_data"]["user_id"])
    return user


@users_router.post("/sign-up/")
async def user_signup_endpoint(user_data: NewUser, session_db: AsyncSession = Depends(get_db)):
    user_service = UserService(UserRepository(SessionDBManager(session_db=session_db)))
    token = await user_service.create_user(user_data=user_data.model_dump())
    return JSONResponse(status_code=status.HTTP_200_OK, content={"token": token})


@users_router.post("/sign-in/")
async def user_signin_endpoint(user_data: LoginUser, session_db: AsyncSession = Depends(get_db)):
    user_service = UserService(UserRepository(SessionDBManager(session_db=session_db)))
    token = await user_service.login(user_data=user_data.model_dump())
    return JSONResponse(status_code=status.HTTP_200_OK, content={"token": token})


@users_router.patch("/update/account/")
async def update_user_account_endpoint(account_data: UpdateUser, result_token = Depends(verify_token), session_db: AsyncSession = Depends(get_db)):
    user_service = UserService(UserRepository(SessionDBManager(session_db=session_db)))
    await user_service.update_account(user_id=result_token.data["token_data"]["user_id"], account_data=account_data.model_dump(exclude_unset=True))
    return JSONResponse(status_code=status.HTTP_200_OK, content={"ok": True})


@users_router.patch("/update/personal-data/")
async def update_user_personal_data_endpoint(personal_data: PersonalData, result_token: str = Depends(verify_token), session_db: AsyncSession = Depends(get_db)):
    user_service = UserService(UserRepository(SessionDBManager(session_db=session_db)))
    await user_service.update_personal_data(user_id=result_token.data["token_data"]["user_id"], personal_data=personal_data.model_dump(exclude_unset=True))
    return JSONResponse(status_code=status.HTTP_200_OK, content={"ok": True})


@users_router.patch("/update/delivery-data/")
async def update_user_delivery_data_endpoint(delivery_data: DeliveryData, result_token: str = Depends(verify_token), session_db: AsyncSession = Depends(get_db)):
    user_service = UserService(UserRepository(SessionDBManager(session_db=session_db)))
    await user_service.update_personal_data(user_id=result_token.data["token_data"]["user_id"], delivery_data=delivery_data.model_dump(exclude_unset=True))
    return JSONResponse(status_code=status.HTTP_200_OK, content={"ok": True})


@users_router.post("/logout/")
async def logout_user_endpoint(result_token: str = Depends(verify_token)):
    user_service = UserService(UserRepository(SessionDBManager()))
    await user_service.logout(token=result_token.token)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"ok": True})


@users_router.delete("/delete/me/")
async def delete_user_endpoint(result_token: str = Depends(verify_token)):
    pass


router_v1.include_router(users_router)
