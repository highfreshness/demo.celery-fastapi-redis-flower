import os
from celery import Celery

BROKER_URL = os.getenv("BROKER_URL", "redis://localhost")
BACKEND_URL = os.getenv("BACKEND_URL", "redis://localhost")

app = Celery("tasks", broker=BROKER_URL, backend=BACKEND_URL)
