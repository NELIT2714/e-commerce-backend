from fastapi import APIRouter

from project import router_v1
from project.routes.manufacturers.dto import NewManufacturer, UpdateManufacturer

carts_router = APIRouter(prefix="/carts", tags=["Cart"])


@carts_router.get("/get/")
async def get_carts_endpoint():
    pass


@carts_router.get("/get/{user_id}/")
async def get_cart_endpoint(user_id: int):
    pass


@carts_router.delete("/clear/{user_id}/")
async def delete_manufacturer_endpoint(user_id: int):
    pass


router_v1.include_router(carts_router)
