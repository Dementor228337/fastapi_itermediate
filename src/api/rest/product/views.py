from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.api.rest.product.decorators import handle_product_errors
from src.api.rest.user.decorators import check_permissions_decorator

from src.core.permissions import Permissions
from src.core.product.services import product_service
from src.dependencies import get_current_user
from src.products.manager import product_manager


products_router = APIRouter(prefix='/products', tags=["products"])

class ProductSchema(BaseModel):
    id: int
    name: str
    price: float

@products_router.post("")
@check_permissions_decorator([Permissions.ADD_PRODUCT.value])
@handle_product_errors
async def create_product(product: ProductSchema, current_user=Depends(get_current_user)):
    product_service.add(product)
    return {'created': f"{product.name} by {current_user.email}"}

@products_router.get("/{product_id}")
@check_permissions_decorator([Permissions.VIEW_PRODUCT.value])
@handle_product_errors
async def get_product(product_id: int, current_user=Depends(get_current_user)):

    return product_service.get(product_id)


@products_router.put("/{product_id}")
@check_permissions_decorator([Permissions.UPDATE_PRODUCT.value])
@handle_product_errors
async def update_product(product_id: int, product: ProductSchema, current_user=Depends(get_current_user)):

    product_service.update(product_id, product)

    return {'updated': f"{product.name} by {current_user.email}"}

@products_router.delete("/{product_id}")
@check_permissions_decorator([Permissions.DELETE_PRODUCT.value])
@handle_product_errors
async def delete_product(product_id: int, current_user=Depends(get_current_user)):

    product_service.delete(product_id)

    return {'deleted': f"{product_id} by {current_user.email}"}

@products_router.get("")
async def get_all():
    return product_manager.products

