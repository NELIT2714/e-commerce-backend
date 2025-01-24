from fastapi import APIRouter
from fastapi.responses import JSONResponse

from project import router_v1
from project.database.crud.admins import create_admin, login, get_admin
from project.database.crud.articles import get_articles, get_article, create_article, update_article, delete_article
from project.routes.admins.dto import NewAdmin, LoginAdmin

admins_router = APIRouter(prefix="/admins", tags=["Admins"])


@admins_router.get("/get/")
async def get_admins_endpoint():
    admins = await get_admins()
    return JSONResponse(status_code=200, content={"admins": admins})


@admins_router.get("/get/{admin_id}/")
async def get_admin_endpoint(admin_id: int):
    admin = await get_admin(admin_id)
    return JSONResponse(status_code=200, content={"admin": admin})


@admins_router.post("/login/")
async def update_admin_endpoint(admin_data: LoginAdmin):
    token = await login(admin_data.model_dump(exclude_none=True))
    return JSONResponse(status_code=200, content={"token": token})


@admins_router.post("/create/")
async def create_admin_endpoint(admin_data: NewAdmin):
    created_admin = await create_admin(admin_data.model_dump())
    return JSONResponse(status_code=200, content={"created_admin": created_admin})


@admins_router.patch("/update/{admin_id}/")
async def update_admin_endpoint(admin_id: int, admin_data: NewAdmin):
    updated_admin = await update_admin(admin_id, admin_data.model_dump(exclude_none=True))
    return JSONResponse(status_code=200, content={"updated_admin": updated_admin})


@admins_router.delete("/delete/{admin_id}/")
async def delete_admin_endpoint(admin_id: int):
    admins = await delete_admin(admin_id)
    return JSONResponse(status_code=200, content={"admins": admins})


router_v1.include_router(admins_router)
