import os
from celery import Celery
from time import sleep

BROKER_URL = os.getenv("BROKER_URL", "redis://localhost")
BACKEND_URL = os.getenv("BACKEND_URL", "redis://localhost")

celery_app = Celery("tasks", broker=BROKER_URL, backend=BACKEND_URL)

TIME = os.getenv("SLEEP_TIME", "5")


@celery_app.task(name="add")
def add(a: int, b: int) -> int:
    answer = a + b
    sleep(int(TIME))
    return answer
