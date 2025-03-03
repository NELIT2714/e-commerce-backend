from fastapi import APIRouter
from fastapi.responses import JSONResponse

from project import router_v1
from project.database.crud.categories import get_category, create_category, get_categories, update_category, \
    delete_category
from project.database.crud import CategoriesRepository
from project.routes.categories.dto import NewCategory, UpdateCategory

categories_router = APIRouter(prefix="/categories", tags=["Categories"])


@categories_router.get("/get/")
async def get_categories_endpoint():
    categories = await get_categories(dump=True)
    return JSONResponse(status_code=200, content={"categories": categories})


@categories_router.get("/get/{category_id}/")
async def get_category_endpoint(category_id: int):
    categories_repository = CategoriesRepository()
    category = await categories_repository.get_category(category_id=category_id)
    return category
    # return JSONResponse(status_code=200, content={"category": category})


@categories_router.post("/create/")
async def create_category_endpoint(category_data: NewCategory):
    created_category = await create_category(category_data.model_dump(), dump=True)
    return JSONResponse(status_code=200, content={"created_category": created_category})


@categories_router.patch("/update/{category_id}/")
async def update_category_endpoint(category_id: int, category_data: UpdateCategory):
    updated_category = await update_category(category_id, category_data.model_dump(exclude_unset=True), dump=True)
    return JSONResponse(status_code=200, content={"updated_category": updated_category})


@categories_router.delete("/delete/{category_id}/")
async def delete_category_endpoint(category_id: int):
    categories = await delete_category(category_id, dump=True)
    return JSONResponse(status_code=200, content={"categories": categories})


router_v1.include_router(categories_router)
