from functools import wraps

from fastapi import HTTPException, status

from src.core.product.exceptions import ProductAlreadyExistsError, ProductNotFoundError


def handle_product_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (ProductAlreadyExistsError, ProductNotFoundError) as error:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return wrapper