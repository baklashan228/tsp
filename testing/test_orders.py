from faker import Faker
fake=Faker()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Base, Order, User, Product, Orderitem

engine = create_engine('postgresql://postgres:zolozz@localhost/labs')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def test_add_orders():
    user = User(username=fake.name(), email=fake.email())
    product = Product(name='Nike Mercurial', description='Latest model boots', price=699.99, stock=50)

    session.add(user)
    session.add(product)
    session.commit()

    order = Order(user=user, status='Completed', total_amount=699.99)

    session.add(order)

    order_item = Orderitem(order=order, product=product, quantity=1, price=product.price)

    session.add(order_item)
    session.commit()

    orders = session.query(Order).all()

session.close()
