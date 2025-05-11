from fastapi import APIRouter
from typing import List
import sys
import os

# Добавляем путь к директории с модулем
sys.path.append(os.path.abspath('/'))

# Теперь вы можете импортировать модуль
from Myshop.cruda import create_product, read_products, update_product, delete_product  # Импортируйте ваш CRUD модуль

router = APIRouter()

@router.post("/products/")
def create_product(name: str, price: float, description: str = None):
    create_product(name, price, description)
    return {"message": "Product created successfully"}

@router.get("/products/", response_model=List[dict])
def read_products():
    products = read_products()
    return products

@router.put("/products/{product_id}")
def update_product(product_id: int, name: str, price: float, description: str = None):
    update_product(product_id, name, price, description)
    return {"message": "Product updated successfully"}

@router.delete("/products/{product_id}")
def delete_product(product_id: int):
    delete_product(product_id)
    return {"message": "Product deleted successfully"}
