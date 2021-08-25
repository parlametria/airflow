SHELL := /bin/bash

webserver:
	airflow webserver --port 8080

scheduler:
	airflow scheduler
