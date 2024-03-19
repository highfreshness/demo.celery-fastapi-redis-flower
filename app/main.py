from fastapi import FastAPI
from tasks import sentence_summarize

app = FastAPI()


@app.post("/inference")
async def inference(sentence: str) -> dict:
    result = sentence_summarize.delay(sentence)  # Redis로 전송
    summarization = result.get(timeout=10)  # 10초 동안 작업의 완료를 기다림
    return {"Summarization": summarization}


@app.post("/inference_test")
async def inference_test(sentence: str) -> dict:
    result = sentence_summarize(sentence)
    return {"Summarization": result}
