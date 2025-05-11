from fastapi import APIRouter
from typing import List
import sys
import os

sys.path.append(os.path.abspath('/'))

from Myshop.cruda import create_category, read_categories, update_category, delete_category
router = APIRouter()

# Создание категории
@router.post("/categories/")
def create_category_endpoint(category_id: int, name: str, description: str):
    create_category(category_id, name, description)
    return {"message": "Category created successfully"}

# Чтение всех категорий
@router.get("/categories/", response_model=List[dict])
def read_categories_endpoint():
    categories = read_categories()
    return categories

# Обновление категории
@router.put("/categories/{category_id}")
def update_category_endpoint(category_id: int, name: str, description: str):
    update_category(category_id, name, description)
    return {"message": "Category updated successfully"}

# Удаление категории
@router.delete("/categories/{category_id}")
def delete_category_endpoint(category_id: int):
    delete_category(category_id)
    return {"message": "Category deleted successfully"}
