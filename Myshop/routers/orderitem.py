from fastapi import APIRouter
from typing import List
import sys
import os

# Добавляем путь к директории с модулем
sys.path.append(os.path.abspath('/'))

# Теперь вы можете импортировать модуль
from Myshop.cruda import create_orderitem, read_orderitems, update_orderitem, delete_orderitem  # Импортируйте ваш CRUD модуль

router = APIRouter()

@router.post("/orderitems/")
def create_orderitem(order_id: int, product_id: int, quantity: int):
    create_orderitem(order_id, product_id, quantity)
    return {"message": "Order item created successfully"}

@router.get("/orderitems/", response_model=List[dict])
def read_orderitems():
    order_items = read_orderitems()
    return order_items

@router.put("/orderitems/{order_item_id}")
def update_orderitem(order_item_id: int, order_id: int, product_id: int, quantity: int):
    update_orderitem(order_item_id, order_id, product_id, quantity)
    return {"message": "Order item updated successfully"}

@router.delete("/orderitems/{order_item_id}")
def delete_orderitem(order_item_id: int):
    delete_orderitem(order_item_id)
    return {"message": "Order item deleted successfully"}
