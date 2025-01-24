from fastapi import APIRouter
from fastapi.responses import JSONResponse

from project import router_v1
from project.database.crud.manufacturers import get_manufacturers, get_manufacturer, create_manufacturer, \
    update_manufacturer, delete_manufacturer
from project.routes.manufacturers.dto import NewManufacturer, UpdateManufacturer

manufacturers_router = APIRouter(prefix="/manufacturers", tags=["Manufacturers"])


@manufacturers_router.get("/get/")
async def get_manufacturers_endpoint():
    manufacturers = await get_manufacturers(dump=True)
    return JSONResponse(status_code=200, content={"manufacturers": manufacturers})


@manufacturers_router.get("/get/{manufacturer_id}/")
async def get_manufacturer_endpoint(manufacturer_id: int):
    manufacturer = await get_manufacturer(manufacturer_id, dump=True)
    return JSONResponse(status_code=200, content={"manufacturer": manufacturer})


@manufacturers_router.post("/create/")
async def create_manufacturer_endpoint(manufacturer_data: NewManufacturer):
    created_manufacturer = await create_manufacturer(manufacturer_data.model_dump(), dump=True)
    return JSONResponse(status_code=200, content={"created_manufacturer": created_manufacturer})


@manufacturers_router.patch("/update/{manufacturer_id}/")
async def update_manufacturer_endpoint(manufacturer_id: int, manufacturer_data: UpdateManufacturer):
    updated_manufacturer = await update_manufacturer(manufacturer_id, manufacturer_data.model_dump(exclude_unset=True), dump=True)
    return JSONResponse(status_code=200, content={"updated_manufacturer": updated_manufacturer})


@manufacturers_router.delete("/delete/{manufacturer_id}/")
async def delete_manufacturer_endpoint(manufacturer_id: int):
    manufacturers = await delete_manufacturer(manufacturer_id, dump=True)
    return JSONResponse(status_code=200, content={"manufacturers": manufacturers})


router_v1.include_router(manufacturers_router)
