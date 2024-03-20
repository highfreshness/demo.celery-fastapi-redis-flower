- Celery worker 실행
	celery -A tasks worker --loglevel=INFO

- Celery flower 실행
	Celery -A tasks flower

- {task}.delay의 결과는 작업 ID를 반환 반환된 객체를 가지고 상태를 확인하거나 결과를 출력할 수 있음
	result = add.delay(4,4)
	result.ready() -> 작업 결과 여부
	result.get() -> 작업 결과

- fastapi에서 task를 넘기고 10초가 지나가면 worker의 결과가 성공이어도 500에러가 난다.
- worker 수를 늘리려면 docker compose up -d --scale worker=3 처럼 scale 옵션을 줘야 한다.