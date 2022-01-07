from datetime import datetime, timedelta

from airflow import DAG

from docker.types import Mount

from tasks.process_entidades import process_entidades_tasks
from dags import execute_tasks_in_sequence

default_args = {
    "owner": "airflow",
    "description": "Docker process_entidades",
    "depend_on_past": False,
    "start_date": datetime(2021, 5, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "process_entidades",
    default_args=default_args,
    schedule_interval="0 12 * * 6",  # Update parlamentares every friday at 12:00 UTC
    catchup=False,
) as dag:
    mounts = [Mount("/agora-digital/leggo_data", "leggo_data")]

    tasks = [
        *process_entidades_tasks(mounts)
    ]

    execute_tasks_in_sequence(tasks)
