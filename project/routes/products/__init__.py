from fastapi import APIRouter
from fastapi.responses import JSONResponse

from project import router_v1
from project.routes.products.dto import NewProduct, UpdateProduct

products_router = APIRouter(prefix="/products", tags=["Products"])


@products_router.get("/get/")
async def get_products_endpoint():
    pass


@products_router.get("/get/{product_id}/")
async def get_product_endpoint(product_id: int):
    pass


@products_router.post("/create/")
async def create_product_endpoint(product_data: NewProduct):
    return JSONResponse({"product": product_data.model_dump()})
    # print(product_data.model_dump())


# @products_router.patch("/update/{product_id}/", response_model=None)
# async def update_product_endpoint(product_id: int, product_data: UpdateProduct):
#     pass


@products_router.delete("/delete/{product_id}/")
async def delete_product_endpoint(product_id: int):
    pass


router_v1.include_router(products_router)
