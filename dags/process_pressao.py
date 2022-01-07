from datetime import datetime, timedelta

from airflow import DAG

from docker.types import Mount

from tasks.process_pressao import process_pressao_tasks
from dags import execute_tasks_in_sequence

default_args = {
    "owner": "airflow",
    "description": "Docker process_pressao",
    "depend_on_past": False,
    "start_date": datetime(2021, 5, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "process_pressao",
    default_args=default_args,
    schedule_interval="0 7 * * *",  # Run pressao pipeline 7:00 UTC
    catchup=False,
) as dag:
    mounts = [Mount("/leggo-trends/leggo_data", "leggo_data")]

    tasks = [
        *process_pressao_tasks(mounts)
    ]

    execute_tasks_in_sequence(tasks)
