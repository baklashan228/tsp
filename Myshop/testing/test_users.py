from faker import Faker
fake=Faker()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Myshop.app import Base

# Создание подключения к базе данных
engine = create_engine('postgresql://postgres:zolozz@localhost/labs')
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

def test_add_users():
    user1 = User(username=fake.name(), email=fake.email())
    user2 = User(username=fake.name(), email=fake.email())

    session.add(user1)
    session.add(user2)
    session.commit()

    users = session.query(User).all()


def test_read_users():
    users = session.query(User).all()
    for user in users:
        print(f'User ID: {user.user_id}, Username: {user.username}, Email: {user.email}')
from faker import Faker
fake=Faker()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Myshop.app import Base, User, Order, Review, Product, Orderitem

# Создание подключения к базе данных
engine = create_engine('postgresql://postgres:zolozz@localhost/labs')
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

def test_add_users():
    user1 = User(username=fake.name(), email=fake.email())
    user2 = User(username=fake.name(), email=fake.email())

    session.add(user1)
    session.add(user2)
    session.commit()

    users = session.query(User).all()

def get_orders_info(user_id=None):
    if user_id:
        # Получаем заказы конкретного пользователя
        orders = session.query(Order).filter(Order.user_id == user_id).all()
    else:
        # Получаем все заказы
        orders = session.query(Order).all()

    if orders:
        for order in orders:
            print(f'Order ID: {order.order_id}, User ID: {order.user_id}, Status: {order.status}, Total Amount: {order.total_amount}')
            # Получаем товары в заказе
            if hasattr(order, 'order_items'):
                for order_item in order.order_items:
                    product = session.query(Product).filter(Product.product_id == order_item.product_id).first()
                    if product:
                        print(f'    Product ID: {product.product_id}, Name: {product.name}, Quantity: {order_item.quantity}, Price: {order_item.price}')
            else:
                print('    Нет товаров в заказе.')
    else:
        print(f'Нет заказов для пользователя ID {user_id}.' if user_id else 'Нет заказов.')





def test_read_users():
    users = session.query(User).all()
    for user in users:
        print(f'User ID: {user.user_id}, Username: {user.username}, Email: {user.email}')



def get_last_order_products(user_id):
    # Получаем последний заказ пользователя
    last_order = session.query(Order).filter(Order.user_id == user_id).order_by(Order.order_id.desc()).first()

    if last_order:
        # Получаем связанные товары
        if hasattr(last_order, 'products'):
            products = last_order.products
            print(f'Товары последнего заказа пользователя ID {user_id}:')
            for product in products:
                print(f'Product ID: {product.product_id}, Name: {product.name}, Price: {product.price}')
        else:
            print(f'У пользователя ID {user_id} нет товаров в последнем заказе.')
        session.query(Orderitem).filter(Orderitem.order_id == last_order.order_id).delete()
    else:
        print(f'У пользователя ID {user_id} нет заказов.')


    # Удаление всех заказов пользователя
    session.query(Order).filter(Order.user_id == user_id).delete()
    session.commit()
    # Сохраняем изменения

    new_order = Order(user_id=user_id, status='Pending',
                      total_amount=0.00)  # Изначально total_amount можно установить в 0
    session.add(new_order)
    new_order1 = Order(user_id=user_id, status='Pending',
                      total_amount=0.00)  # Изначально total_amount можно установить в 0
    session.add(new_order1)
    session.commit()

    # Теперь создаем объект Orderitem
    order_item = Orderitem(order_id=new_order.order_id, product_id=1, quantity=1,
                           price=90.0)
    order_item1 = Orderitem(order_id=new_order1.order_id, product_id=2, quantity=1,
                           price=90.0)
    # Добавляем Orderitem в заказ
    new_order.order_items.append(order_item)
    new_order.order_items.append(order_item1)


    # Пример товаров для новых заказов (предполагается, что у вас есть товары с ID 1 и 2)
    product1 = session.query(Product).filter(Product.product_id == 1).first()
    product2 = session.query(Product).filter(Product.product_id == 2).first()

    if product1 is None or product2 is None:
        print('Один или оба товара не найдены.')
        return

    new_order1.order_items.append(order_item)
    new_order.order_items.append(order_item1)


    try:
        # Добавляем новые заказы в сессию
        session.add(new_order1)
        session.add(new_order)
        session.commit()  # Сохраняем изменения
        print(f'Добавлены новые заказы для пользователя ID {user_id}.')
    except Exception as e:
        print(f'Ошибка при добавлении новых заказов: {e}')
        session.rollback()  # Откат изменений в случае ошибки

# Пример вызова функци




def get_users_who_left_reviews(product_id):
    # Получаем всех пользователей, которые оставили отзывы
    users_with_reviews = session.query(User).join(Review).filter(Review.product_id == product_id).all()

    if users_with_reviews:
        print('Пользователи, оставившие отзывы:')
        for user in users_with_reviews:
            print(f'User ID: {user.user_id}, Username: {user.username}, Email: {user.email}')
    else:
        print('Нет пользователей, оставивших отзывы.')




# Закрытие сессии
session.close()



def get_last_order_products(user_id):
    # Получаем последний заказ пользователя
    last_order = session.query(Order).filter(Order.user_id == user_id).order_by(Order.order_id.desc()).first()

    if last_order:
        # Получаем связанные товары
        if hasattr(last_order, 'products'):
            products = last_order.products
            print(f'Товары последнего заказа пользователя ID {user_id}:')
            for product in products:
                print(f'Product ID: {product.product_id}, Name: {product.name}, Price: {product.price}')
        else:
            print(f'У пользователя ID {user_id} нет товаров в последнем заказе.')
        session.query(Orderitem).filter(Orderitem.order_id == last_order.order_id).delete()
    else:
        print(f'У пользователя ID {user_id} нет заказов.')


    # Удаление всех заказов пользователя
    session.query(Order).filter(Order.user_id == user_id).delete()
    session.commit()
    # Сохраняем изменения

    new_order = Order(user_id=user_id, status='Pending',
                      total_amount=0.00)  # Изначально total_amount можно установить в 0
    session.add(new_order)
    new_order1 = Order(user_id=user_id, status='Pending',
                      total_amount=0.00)  # Изначально total_amount можно установить в 0
    session.add(new_order1)
    session.commit()

    # Теперь создаем объект Orderitem
    order_item = Orderitem(order_id=new_order.order_id, product_id=1, quantity=1,
                           price=90.0)
    order_item1 = Orderitem(order_id=new_order1.order_id, product_id=2, quantity=1,
                           price=90.0)
    # Добавляем Orderitem в заказ
    new_order.order_items.append(order_item)
    new_order.order_items.append(order_item1)


    # Пример товаров для новых заказов (предполагается, что у вас есть товары с ID 1 и 2)
    product1 = session.query(Product).filter(Product.product_id == 1).first()
    product2 = session.query(Product).filter(Product.product_id == 2).first()

    if product1 is None or product2 is None:
        print('Один или оба товара не найдены.')
        return

    new_order1.order_items.append(order_item)
    new_order.order_items.append(order_item1)


    try:
        # Добавляем новые заказы в сессию
        session.add(new_order1)
        session.add(new_order)
        session.commit()  # Сохраняем изменения
        print(f'Добавлены новые заказы для пользователя ID {user_id}.')
    except Exception as e:
        print(f'Ошибка при добавлении новых заказов: {e}')
        session.rollback()  # Откат изменений в случае ошибки

# Пример вызова функци




def get_users_who_left_reviews(product_id):
    # Получаем всех пользователей, которые оставили отзывы
    users_with_reviews = session.query(User).join(Review).filter(Review.product_id == product_id).all()

    if users_with_reviews:
        print('Пользователи, оставившие отзывы:')
        for user in users_with_reviews:
            print(f'User ID: {user.user_id}, Username: {user.username}, Email: {user.email}')
    else:
        print('Нет пользователей, оставивших отзывы.')




# Закрытие сессии
session.close()


