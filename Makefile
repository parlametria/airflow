SHELL := /bin/bash

# =========================== LOCAL ENV COMMANDS ===============================
local-webserver:
	airflow webserver --port 8080

local-scheduler:
	airflow scheduler

# =========================== DEV DOCKER ENV COMMANDS ===============================
dev-build:
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
