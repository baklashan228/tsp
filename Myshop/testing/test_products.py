from faker import Faker
fake=Faker()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Myshop.app import Base, Product, Category

engine = create_engine('postgresql://postgres:zolozz@localhost/labs')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def test_add_products():
    category = Category(name=fake.name(), description=fake.name())
    session.add(category)
    session.commit()

    product1 = Product(name='Nike Mercurial', description='Latest model boots', price=699.99, stock=50, category=category)
    product2 = Product(name='Adidas Predator', description='High-performance boots', price=999.99, stock=30, category=category)

    session.add(product1)
    session.add(product2)
    session.commit()

    products = session.query(Product).all()


session.close()
