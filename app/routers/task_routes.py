from .. import models, schemas,oauth2
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import Optional,List
from sqlalchemy import func

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis.asyncio import Redis
from ..queue import celery_app, divide

router = APIRouter(
    prefix="/tasks",
    tags=['Tasks']
)

@router.post("/divide")
def api_create_divide_task(request: schemas.TaskRequestDivide,db: Session = Depends(get_db)):
    
    task = divide.delay(request.first, request.second)

    async_id = task.id
    # create_task(db=db,async_id=async_id,first=request.first,second=request.second)
    return {"async_id":async_id}


@router.get('/results/{async_id}')
def api_get_divide_result(async_id: str):
    task = celery_app.AsyncResult(async_id)
    return {
            "status":task.status,
            "result":task.result
            }