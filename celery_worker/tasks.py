import os
import time
from celery import Celery

BROKER_URL = os.getenv("BROKER_URL", "redis://localhost")
BACKEND_URL = os.getenv("BACKEND_URL", "redis://localhost")

app = Celery("tasks", broker=BROKER_URL, backend=BACKEND_URL)

TIME = os.getenv("SLEEP_TIME", "5")


@app.task
def add(a: int, b: int) -> int:
    answer = a + b
    time.sleep(int(TIME))
    return answer
