import json

# Пример данных для записи
data_to_save = {
    "users": [
        {"user_id": 1, "username": "john_doe", "email": "john@example.com"},
        {"user_id": 2, "username": "jane_doe", "email": "jane@example.com"}
    ]
}

# Запись данных в JSON-файл
with open('data.json', 'w') as file:
    json.dump(data_to_save, file, indent=4)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myshops import Base, User, Category, Product, Review, Order, Orderitem  # Импортируйте ваши модели

# Создание подключения к базе данных
engine = create_engine('postgresql://postgres:zolozz@localhost/labs')  # Замените на вашу строку подключения
Base.metadata.create_all(engine)  # Создание таблиц

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Создание тестовых пользователей
user1 = User(username='nllllkkl_o_', email='nla.gjhihijkukyucom')
user2 = User(username='_gyhhhjjgkga_', email='la.cghjhkkllllhkom')

# Добавление пользователей в сессию
session.add(user1)
session.add(user2)

##### считывание пользователя из базы
# Считывание пользователей из базы
users = session.query(User).all()  # Получаем всех пользователей


# Создание тестовых категорий,,,
category1 = Category(name=' -shinkjjjnkkknkjjjrts', description='rnic dejjivll;ices and gadgets')
category2 = Category(name='joolnllmnknk', description='arous gensoljlkojjf books')

# Добавление категорий в сессию
session.add(category1)
session.add(category2)

# Создание тестовых продуктов
product1 = Product(name='nike mercurial', description='Latest model boots', price=699.99, stock=50, category=category1)
product2 = Product(name='adidas predator', description='High-performance boots', price=999.99, stock=30, category=category1)
product3 = Product(name='Real Madrid t-shirt', description='GOAT', price=29.99, stock=100, category=category2)

# Добавление продуктов в сессию
session.add(product1)
session.add(product2)
session.add(product3)

# Создание тестовых отзывов
review1 = Review(product=product1, user=user1, rating=5, comment='Good!')
review2 = Review(product=product2, user=user2, rating=4, comment='Very good')
review3 = Review(product=product3, user=user1, rating=5, comment='Excellent')

# Добавление отзывов в сессию
session.add(review1)
session.add(review2)
session.add(review3)

# Создание тестового заказа
order1 = Order(user=user1, status='Completed', total_amount=729.98)  # Например, сумма заказа включает продукт и его стоимость

# Добавление заказа в сессию
session.add(order1)

# Создание тестовых элементов заказа
order_item1 = Orderitem(order=order1, product=product1, quantity=1, price=product1.price)
order_item2 = Orderitem(order=order1, product=product3, quantity=2, price=product3.price)

# Добавление элементов заказа в сессию
session.add(order_item1)
session.add(order_item2)

for user in users:
    # Получаем отзывы для каждого пользователя
    reviews = session.query(Review).filter_by(user=user1)
    for review in reviews:
        print(f'Review ID: {review.review_id}, Product ID: {review.product_id}, Rating: {review.rating}, Comment: {review.comment}, Created At: {review.created_at}')

# Сохранение всех изменений в базе данных
session.commit()

# Закрытие сессии
session.close()

print("Тестовые данные успешно добавлены в базу данных.")
