from fastapi import APIRouter
from typing import List
import sys
import os

# Добавляем путь к директории с модулем
sys.path.append(os.path.abspath('/'))

# Теперь вы можете импортировать модуль
from Myshop.cruda import create_user, read_users, update_user, delete_user


router = APIRouter()

@router.post("/users/")
def create_user(username: str, email: str):
    create_user(username, email)
    return {"message": "User created successfully"}

@router.get("/users/", response_model=List[dict])
def read_users():
    users = read_users()
    return users

@router.put("/users/{user_id}")
def update_user(user_id: int, username: str, email: str):
    update_user(user_id, username, email)
    return {"message": "User updated successfully"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    delete_user(user_id)
    return {"message": "User deleted successfully"}
