from faker import Faker
fake=Faker()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import Base, Review, User, Product

engine = create_engine('postgresql://postgres:zolozz@localhost/labs')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_reviews_info():
    reviews = session.query(Review).all()

    if reviews:
        for review in reviews:
            user = session.query(User).filter(User.user_id  == review.user_id).first()
            product = session.query(Product).filter(Product.product_id == review.product_id).first()

            user_info = f'Username: {user.username}, Email: {user.email}' if user else 'Unknown User'
            product_info = f'Product Name: {product.name}, Price: {product.price}' if product else 'Unknown Product'

            print(f'Review ID: {review.review_id}, Rating: {review.rating}, Comment: "{review.comment}"')
            print(f'    {user_info}')
            print(f'    {product_info}')
    else:
        print('Нет ревью.')

def test_add_reviews():
    user = User(username=fake.name(), email=fake.name())
    product = Product(name='Nike Mercurial', description='Latest model boots', price=699.99, stock=50)

    session.add(user)
    session.add(product)
    session.commit()

    review1 = Review(product=product, user=user, rating=5, comment='Good!')

    session.add(review1)
    session.commit()

    reviews = session.query(Review).all()



session.close()
