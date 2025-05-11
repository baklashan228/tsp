from fastapi import APIRouter
from typing import List
import sys
import os

# Добавляем путь к директории с модулем
sys.path.append(os.path.abspath('/'))

# Теперь вы можете импортировать модуль
from Myshop.cruda import create_order, read_orders, update_order, delete_order  # Импортируйте ваш CRUD модуль

router = APIRouter()

@router.post("/orders/")
def create_order(user_id: int, product_id: int, quantity: int):
    create_order(user_id, product_id, quantity)
    return {"message": "Order created successfully"}

@router.get("/orders/", response_model=List[dict])
def read_orders():
    orders = read_orders()
    return orders

@router.put("/orders/{order_id}")
def update_order(order_id: int, user_id: int, product_id: int, quantity: int):
    update_order(order_id, user_id, product_id, quantity)
    return {"message": "Order updated successfully"}

@router.delete("/orders/{order_id}")
def delete_order(order_id: int):
    delete_order(order_id)
    return {"message": "Order deleted successfully"}
