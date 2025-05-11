from faker import Faker
fake=Faker()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Myshop.app import Base, Category

engine = create_engine('postgresql://postgres:zolozz@localhost/labs')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def test_add_categories():
    category1 = Category(name=fake.name(), description=fake.name())
    category2 = Category(name=fake.name(), description=fake.name())

    session.add(category1)
    session.add(category2)
    session.commit()

    categories = session.query(Category).all()


session.close()
