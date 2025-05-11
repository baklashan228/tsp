import json
from test_users import get_users_who_left_reviews
from test_users import test_add_users
from test_users import test_read_users
from test_users import get_last_order_products
from test_reviews import get_reviews_info
from test_products import test_add_products
from test_orders import test_add_orders
from test_categories import test_add_categories
from fastapi import FastAPI
from Myshop.routers import user

app = FastAPI()

app.include_router(user.router)

# Запись данных в JSON-файл (если это необходимо)
data_to_save = {
    "users": [
        {"user_id": 1, "username": "johndffddffd_doe", "email": "john@dfdfdfdfdfexample.com"},
        {"user_id": 2, "username": "jane_dfdfdfdfdfdfdoe", "email": "jane@fddfdfdfdfexample.com"}
    ]
}

with open('data.json', 'w') as file:
    json.dump(data_to_save, file, indent=4)

# Выполнение тестов
get_users_who_left_reviews(product_id=7)
#get_orders_info()
get_reviews_info()
#get_last_order_products(user_id=1)
#test_add_users()
#test_read_users()
#test_add_categories()
test_add_products()
#test_add_reviews()
test_add_orders()

print("Тесты успешно выполнены.")






