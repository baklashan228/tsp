from fastapi import APIRouter
from typing import List
import sys
import os


sys.path.append(os.path.abspath('/'))

from Myshop.cruda import create_review, read_reviews, update_review, delete_review  # Импортируйте ваш CRUD модуль

router = APIRouter()

@router.post("/reviews/")
def create_review(product_id: int, user_id: int, rating: int, comment: str = None):
    create_review(product_id, user_id, rating, comment)
    return {"message": "Review created successfully"}

@router.get("/reviews/", response_model=List[dict])
def read_reviews():
    reviews = read_reviews()
    return reviews

@router.put("/reviews/{review_id}")
def update_review(review_id: int, rating: int, comment: str = None):
    update_review(review_id, rating, comment)
    return {"message": "Review updated successfully"}

@router.delete("/reviews/{review_id}")
def delete_review(review_id: int):
    delete_review(review_id)
    return {"message": "Review deleted successfully"}
