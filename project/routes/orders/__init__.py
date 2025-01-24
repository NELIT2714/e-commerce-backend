from fastapi import APIRouter

from project import router_v1
from project.routes.manufacturers.dto import NewManufacturer, UpdateManufacturer

manufacturers_router = APIRouter(prefix="/manufacturers", tags=["Manufacturers"])


@manufacturers_router.get("/get/")
async def get_manufacturers_endpoint():
    pass


@manufacturers_router.get("/get/{manufacturer_id}/")
async def get_manufacturer_endpoint(manufacturer_id: int):
    pass


@manufacturers_router.post("/create/")
async def create_manufacturer_endpoint(manufacturer_data: NewManufacturer):
    pass


@manufacturers_router.patch("/update/{manufacturer_id}/")
async def update_manufacturer_endpoint(manufacturer_id: int, manufacturer_data: UpdateManufacturer):
    pass


@manufacturers_router.delete("/delete/{manufacturer_id}/")
async def delete_manufacturer_endpoint(manufacturer_id: int):
    pass


router_v1.include_router(manufacturers_router)
