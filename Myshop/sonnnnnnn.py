import json
# Запись данных в JSON-файл
with open('data.json', 'w') as file:
    json.dump(data_to_save, file, indent=4)
from myshops import Review  # Импортируйте ваши модели

for user in users:
    # Получаем отзывы для каждого пользователя
    reviews = session.query(Review).filter_by(user=user1)
    for review in reviews:
        print(f'Review ID: {review.review_id}, Product ID: {review.product_id}, Rating: {review.rating}, Comment: {review.comment}, Created At: {review.created_at}')
