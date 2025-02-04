from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from project import logger, router_v1
from project.database.crud.UserRepository import get_user, sign_in, sign_up, update_account, update_delivery_data, update_personal_data
from project.functions import verify_token
from project.routes.users.dto import LoginUser, NewUser, UpdateUser, PersonalData, DeliveryData
from project.schemas.user import UserOut

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/get/me/", response_model=UserOut)
async def get_user_endpoint(result_token: str = Depends(verify_token)):

    user = await get_user(user_id=result_token.data["token_data"]["user_id"], dump=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"user": user})


@users_router.post("/sign-up/")
async def user_signup_endpoint(user_data: NewUser):
    
    return await user_service.get_user(user_id)
    # token = await sign_up(user_data.model_dump())
    # return JSONResponse(status_code=status.HTTP_200_OK, content={"token": token})


@users_router.post("/sign-in/")
async def user_signin_endpoint(user_data: LoginUser):
    token = await sign_in(user_data.model_dump())
    return JSONResponse(status_code=status.HTTP_200_OK, content={"token": token})


@users_router.patch("/update/account/")
async def update_user_account_endpoint(account_data: UpdateUser, result_token = Depends(verify_token)):
    await update_account(user_id=result_token.data["token_data"]["user_id"], account_data=account_data.model_dump(exclude_unset=True))
    return JSONResponse(status_code=status.HTTP_200_OK, content={"ok": True})


@users_router.patch("/update/personal-data/")
async def update_user_personal_data_endpoint(personal_data: PersonalData, result_token: str = Depends(verify_token)):
    await update_personal_data(user_id=result_token.data["token_data"]["user_id"], personal_data=personal_data.model_dump(exclude_unset=True))
    return JSONResponse(status_code=status.HTTP_200_OK, content={"ok": True})


@users_router.patch("/update/delivery-data/")
async def update_user_delivery_data_endpoint(delivery_data: DeliveryData, result_token: str = Depends(verify_token)):
    await update_delivery_data(user_id=result_token.data["token_data"]["user_id"], delivery_data=delivery_data.model_dump(exclude_unset=True))
    return JSONResponse(status_code=status.HTTP_200_OK, content={"ok": True})


@users_router.delete("/delete/me/")
async def delete_user_endpoint(result_token: str = Depends(verify_token)):
    pass


router_v1.include_router(users_router)
