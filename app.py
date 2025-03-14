from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, ForeignKey, TIMESTAMP, CheckConstraint, \
    MetaData
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

# Создаем объект Metadata
metadata = MetaData()

# Создаем базовый класс с использованием этого объекта Metadata
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


    reviews = relationship("Review", back_populates="user")
    orders = relationship("Order", back_populates="user")


class Category(Base):
    __tablename__ = 'Category'

    category_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text)

    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'Product'

    product_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    stock = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('Category.category_id'), nullable=True)

    category = relationship("Category", back_populates="products")
    reviews = relationship("Review", back_populates="product")
    order_items = relationship("Orderitem", back_populates="product")


class Review(Base):
    __tablename__ = 'Review'

    review_id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('Product.product_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'))
    comment = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())

    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")


class Order(Base):
    __tablename__ = 'Order'

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('User.user_id'), nullable=False)
    order_date = Column(TIMESTAMP, server_default=func.now())
    status = Column(String(50), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)

    user = relationship("User", back_populates="orders")
    order_items = relationship("Orderitem", back_populates="order")


class Orderitem(Base):
    __tablename__ = 'Orderitem'

    order_item_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('Order.order_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('Product.product_id'), nullable=False)
    quantity = Column(Integer, CheckConstraint('quantity > 0'))
    price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
