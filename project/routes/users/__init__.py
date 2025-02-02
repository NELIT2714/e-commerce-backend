from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from project import logger, router_v1
from project.database.crud.users import get_user, sign_in, sign_up, update_account
from project.functions import verify_token
from project.routes.users.dto import LoginUser, NewUser, UpdateUser, PersonalData

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/get/{user_id}/")
async def get_user_endpoint(user_id: int, result_token: str = Depends(verify_token)):
    if not user_id == result_token.data["token_data"]["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
    user = await get_user(user_id=user_id, dump=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"user": user})


@users_router.post("/sign-up/")
async def user_signup_endpoint(user_data: NewUser):
    token = await sign_up(user_data.model_dump())
    return JSONResponse(status_code=status.HTTP_200_OK, content={"token": token})


@users_router.post("/sign-in/")
async def user_signin_endpoint(user_data: LoginUser):
    token = await sign_in(user_data.model_dump())
    return JSONResponse(status_code=status.HTTP_200_OK, content={"token": token})


@users_router.patch("/update/account/{user_id}/")
async def update_user_account_endpoint(user_id: int, account_data: UpdateUser, result_token = Depends(verify_token)):
    if not user_id == result_token.data["token_data"]["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
    updated_account = await update_account(user_id=user_id, account_data=account_data.model_dump(exclude_unset=True), token=result_token.token, user_data=account_data.model_dump())


@users_router.patch("/update/personal-data/{user_id}/")
async def update_user_personal_data_endpoint(user_id: int, personal_data: PersonalData, result_token: str = Depends(verify_token)):
    if not user_id == result_token.data["token_data"]["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")
    print(personal_data)


@users_router.delete("/delete/{user_id}/")
async def delete_user_endpoint(user_id: int, result_token: str = Depends(verify_token)):
    pass


router_v1.include_router(users_router)
