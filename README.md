# Celery, FastAPI, Redis, Flower를 이용한 비동기 분산처리 테스트

## 테스트 목적
AI 모델 서빙을 위한 비동기 분산처리 구조 테스트

## 조건
Celery(Worker), FastAPI, Redis(Broker, Backend), Flower(Celery 모니터링)를 모두 개별 환경에서 구동


## 진행 순서
1. Celery 공식문서의 Getting started 기반으로 구현
2. 튜토리얼에서는 FastAPI와 Celery worker를 같은 환경에 구현했기 때문에 Docker compose를 이용해 분리된 환경으로 구성
3. 분리 환경 구성을 기반으로 worker의 수를 늘려 비동기 분산처리 테스트
4. 부하 테스트는 Apache bench로 수행

## Tip
- Celery worker 실행(Celery 인스턴스에 backend, broker가 등록된 상태)
	`celery -A tasks worker --loglevel=INFO`

- Celery flower 실행(Celery 인스턴스에 backend, broker가 등록된 상태)
	`celery -A tasks flower`

- {task}.delay의 결과는 작업 ID를 반환 반환된 객체를 가지고 상태를 확인하거나 결과를 출력할 수도 있고 바로 결과를 받아볼 수 있음
	```python
	result = add.delay(4,4)
	result.ready() # 작업 결과 여부
	result.get(timeout=10) # 작업 결과
	```

- {task}.get()에 timeout을 지정하면 task에서 broker로 작업을 보낸 뒤 timeout만큼 시간이 지나면 HTTP 500 Response를 보낸다.

- worker 수를 늘리고 싶다면 `docker compose up -d --scale worker=3` 처럼 scale 옵션에 숫자를 주면 줘야 한다.