from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Myshop.app import Base

DATABASE_URL = "postgresql://postgres:zolozz@localhost/labs" 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

import psycopg2

def init_db():
    try:
        conn = psycopg2.connect(
            dbname="labs",
            user="postgres",
            password="zolozz",
            host="localhost"
        )
        return conn
    except Exception as e:
        print(f"Connection error: {e}")
        return None

