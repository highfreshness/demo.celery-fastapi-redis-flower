# Celery, FastAPI, Redis, Flower를 이용한 비동기 분산처리 테스트

## 테스트 목적
AI 모델 서빙을 위한 비동기 분산처리 구조 테스트

## 조건
Celery(Worker), FastAPI, Redis(Broker, Backend), Flower(Celery 모니터링)를 모두 개별 환경에서 구동

## 진행 순서
1. Celery 공식문서의 Getting started 기반으로 구현
2. 튜토리얼에서는 FastAPI와 Celery worker를 같은 환경에 구현했지만 모든 기능을 개별환경으로 Docker compose를 이용해 분리 구성
3. 분리 환경 구성을 기반으로 worker의 수를 늘려 비동기 분산처리 테스트
4. 부하 테스트는 Apache bench로 수행

## 필수 설치
Docker, Docker-compose

## 실행 방법
1. git clone https://github.com/highfreshness/demo.celery-fastapi-redis-flower.git && cd demo.celery-fastapi-redis-flower
2. `docker compose up -d && docker compose logs -f` 입력
    - 옵션 추가 시 : `docker compose up -d --build && docker compose logs -f`
     	- --build : 변경 사항이 존재할 때 해당 이미지 build 후 컨테이너 실행
     	- --scale worker={n} : 워커의 수를 n만큼 생성(1개만 필요한 경우 --scale worker={n}을 삭제해도 문제 없음)
3. 테스트
	- localhost(또는 Docker가 실행되는 서버 IP):50601/docs : FastAPI의 Swagger에서 엔드포인트 별 테스트 수행
	- ab -n 100 -c 10  "localhost(또는 Docker가 실행되는 서버IP):50601/inference/id?a=3&b=4" : Apache bench로 동시 요청에 대한 스트레스 테스트 수행
    	- a=3, b=4 라는 인자를 `inference/id`라는 엔드포인트에 100개를 10개씩 나누어 보낸다.
	- localhost(또는 Docker가 실행되는 서버IP):50602 : Celery flower로 worker의 task 처리 상태 등 여러가지 항목들을 UI로 확인 가능


## Tip
- 테스트 시 {task}.delay의 결과를 어떻게 받을 것인가에 따라 요청의 처리속도가 달라지는 것을 확인
	- 요청의 응답으로 ID를 반환(=get() 사용 X)
		- 장점 : 요청의 개수에 관계 없이 빠르게 worker에 분배되며 FastAPI 엔드 포인트에서도 바로 ID를 통해 응답 받을 수 있다.(비동기식 처리가 가능) 
		- 단점 : 유저 입장에서는 ID를 받아서 FastAPI 다른 엔드포인트에서 작업에 대한 상태 값을 직접 확인해 완료 상태일 때 결과를 확인할 수 있다.(유저 편의성 하향)
	- 요청의 응답을 바로 출력(=get() 사용 O)
		- 장점 : 요청 시 작업 처리되는 시간만 기다리면 결과가 바로 보이기 때문에 편의성이 올라간다.
		- 단점 : 요청 시 worker의 개수에 따라 한번에 처리할 수 있는 양이 정해져있으며 요청이 쌓여 처리가 안되면 timeout 시간에 따라 500 HTTP response를 받을 수 있다.

- 기존 FastAPI 컨테이너에서 Celery task를 사용하기 worker 정의가 필요했지만 signature를 사용한다면 task 등록 없이 worker로 작업에 필요한 값만 보낼 수 있게 되었다.
- 병렬처리 능력 향상 방법
  - Celery worker의 concurrency 증가 : 한번에 worker가 처리량 증가
  - Worker container scale 증가 : 실제 워커가 동작하는 컨테이너의 수를 늘려 처리량 증가
  - 여러 방법이 있지만 단일 환경에서 CPU나 기타 자원이 풍부한 경우 worker의 concurrency 증가가 유리할 것으로 보이며 컨테이너 구성 환경에서 단일 CPU, 적은 자원을 활용할 땐 Scale out이 더 유리할 것으로 생각됨.
