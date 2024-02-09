from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import redis
import os
from urllib.parse import urlparse

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# SQLALCHEMY_DATABASE_URL = 'postgres://<username>:<password>@<ip-address/hostname>/<database>'

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# cache = redis.Redis(host=settings.database_hostname, port=settings.redis_port,  decode_responses=True)
# r = redis.from_url(os.environ.get("REDIS_URL"))
    
# url = urlparse(os.environ.get("REDIS_URL"))
# r = redis.Redis(host=url.hostname, port=url.port, password=url.password, ssl=True, ssl_cert_reqs=None)

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost',database='fastapi',
#                            user='postgres',password='123456',cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB connected")
#         break

#     except Exception as error:
#         print("Connecting db failed")
#         print("Error : ",error)
#         time.sleep(2)
