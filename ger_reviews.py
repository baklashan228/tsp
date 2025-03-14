from sqlalchemy.orm import sessionmaker
from app import User, Review  # Импортируйте ваши модели

# Создание подключения к базе данных
engine = create_engine('postgresql://postgres:zolozz@localhost/labs')  # Замените на вашу строку подключения

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Получаем пользователя user1 по username (или user_id)
user1 = session.query(User).filter_by(username='john_doa').first()  # Или используйте user_id

if user1:
    # Получаем отзывы пользователя user1
    user_reviews = session.query(Review).filter_by(user=user1).all()

    # Выводим отзывы
    for review in user_reviews:
        print(f"Review ID: {review.id}, Product ID: {review.product.id}, Rating: {review.rating}, Comment: {review.comment}")
else:
    print("Пользователь не найден.")

# Закрытие сессии
session.close()
