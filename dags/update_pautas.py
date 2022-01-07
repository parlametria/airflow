from datetime import datetime, timedelta

from airflow import DAG

from docker.types import Mount

from tasks.update_pautas import update_pautas_tasks
from dags import execute_tasks_in_sequence

default_args = {
    "owner": "airflow",
    "description": "Docker basic_pipeline",
    "depend_on_past": False,
    "start_date": datetime(2021, 5, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "update_pautas",
    default_args=default_args,
    schedule_interval="30 11 * * 1-5",
    catchup=False,
) as dag:
    mounts = [Mount("/agora-digital/leggo_data", "leggo_data")]

    tasks = [
        *update_pautas_tasks(mounts),
    ]

    execute_tasks_in_sequence(tasks)
