from celery import Celery
import time

celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery_app.task
def divide(x, y):
    time.sleep(10)
    return {"result": x / y}

@celery_app.task
def check():
    return 2

celery_app.conf.beat_schedule = {
 "run-me-every-ten-seconds": {
 "task": "tasks.check",
 "schedule": 10.0
 }
}