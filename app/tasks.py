import os
from celery import Celery
from asyncio import sleep

BROKER_URL = os.getenv("BROKER_URL", "redis://localhost")
BACKEND_URL = os.getenv("BACKEND_URL", "redis://localhost")

app = Celery("tasks", broker=BROKER_URL, backend=BACKEND_URL)

TIME = os.getenv("SLEEP_TIME", "5")


@app.task
async def add(a: int, b: int) -> int:
    answer = a + b
    await sleep(int(TIME))
    return answer
