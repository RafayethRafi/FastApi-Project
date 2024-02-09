import sys
sys.stdout.flush()

from fastapi import FastAPI,Response,status,HTTPException,Depends
# from fastapi.params import Body
# from typing import Optional,List
# from random import randrange
# from sqlalchemy.orm import Session
from . import models,schemas,utils
from .database import engine,SessionLocal,get_db
from .routers import post ,user, auth,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=engine)

import os
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis.asyncio import Redis


app = FastAPI()

@app.on_event("startup")
async def startup():
    redis_connection = Redis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis_connection)



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "khela hobe!!!"}


@app.get("/endpoint", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
async def endpoint():
    return {"msg": "Hello World"}