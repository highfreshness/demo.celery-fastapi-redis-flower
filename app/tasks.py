import os
import nltk

nltk.download("punkt")
from celery import Celery
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model = AutoModelForSeq2SeqLM.from_pretrained("eenzeenee/t5-small-korean-summarization")
tokenizer = AutoTokenizer.from_pretrained("eenzeenee/t5-small-korean-summarization")

BROKER_URL = os.getenv("BROKER_URL", "redis://localhost")
BACKEND_URL = os.getenv("BACKEND_URL", "redis://localhost")

app = Celery("tasks", broker=BROKER_URL, backend=BACKEND_URL)


@app.task
def sentence_summarize(sentence: str) -> str:
    prefix = "summarize: "
    inputs = [prefix + sentence]
    inputs = tokenizer(inputs, max_length=512, truncation=True, return_tensors="pt")
    output = model.generate(
        **inputs, num_beams=3, do_sample=True, min_length=10, max_length=64
    )
    decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    answer = nltk.sent_tokenize(decoded_output.strip())[0]
    return answer
