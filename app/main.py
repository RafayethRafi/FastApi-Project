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


app = FastAPI(title="First Project",
              description="This is a very simple project, with auto docs for the API and everything",
              docs_url="/")

@app.on_event("startup")
async def startup():
    host = settings.redis_host
    port = settings.redis_port
    redis = Redis(
        host=host,
        port=port,
        decode_responses=True,
    )
    await FastAPILimiter.init(redis)


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
# app.include_router(task_router.router)

@app.get("/")
def root():
    return {"message": "khela hobe!!!"}


@app.get("/endpoint", dependencies=[Depends(RateLimiter(times=500, seconds=500))])
async def endpoint():
    return {"msg": "Hello World"}