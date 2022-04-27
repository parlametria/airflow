SHELL := /bin/bash

# =========================== DEV DOCKER COMMANDS ===============================
dev-build:
	docker build -f tasks/process_new_tweets/Dockerfile -t new_tweets tasks/process_new_tweets/
	docker-compose build

dev-webserver:
	docker-compose up -d webserver

dev-scheduler:
	docker-compose up -d scheduler

dev-bash:
	docker-compose run webserver /bin/bash

dev-up:
	make dev-webserver
	make dev-scheduler

# =========================== PRED DOCKER COMMANDS ===============================
prod-init-db:
	docker-compose -f docker-compose.prod.yaml run airflow-webserver airflow db init

prod-bash:
	docker-compose -f docker-compose.prod.yaml run airflow-webserver /bin/bash

prod-build:
	docker-compose -f docker-compose.prod.yaml build

prod-webserver:
	docker-compose -f docker-compose.prod.yaml up airflow-webserver

prod-scheduler:
	docker-compose -f docker-compose.prod.yaml up airflow-scheduler

prod-up:
	make prod-webserver
	make prod-scheduler

down:
	docker-compose down
