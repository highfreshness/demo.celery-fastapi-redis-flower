import os
import uvicorn
from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
from celery import signature, Celery
from celery.result import AsyncResult

app = FastAPI()

BROKER_URL = os.getenv("BROKER_URL", "redis://localhost")
BACKEND_URL = os.getenv("BACKEND_URL", "redis://localhost")

celery_app = Celery("tasks", broker=BROKER_URL, backend=BACKEND_URL)


@app.get("/inference/id")
def inference_id(a: int, b: int) -> dict:
    add_signature = signature("add", args=(a, b), app=celery_app)
    task: AsyncResult = add_signature.delay()
    # 요청 직후 답변 테스트
    # task_result = AsyncResult(task.id, app=celery_app)
    # while True:
    #     if task.state == "SUCCESS":
    #         break
    # return {"Task_ID": task.get()}
    return {"Task_ID": task.id}


@app.get("/inference/result")
def inference_result(id: str) -> dict:
    task_result = AsyncResult(id, app=celery_app)
    # Task의 상태 확인
    if task_result.state == "PENDING":
        # Task가 아직 완료되지 않았습니다.
        return {"message": "Task is still processing..."}
    elif task_result.state == "SUCCESS":
        # Task가 성공적으로 완료되었습니다. 결과를 가져옵니다.
        result = task_result.get()
        return {"Result": result}
    else:
        # Task가 실패하거나 다른 상태일 경우
        print("Task state:", task_result.state)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="info")
