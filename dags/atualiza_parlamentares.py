from datetime import datetime, timedelta

from airflow import DAG

from docker.types import Mount

from tasks.atualiza_parlamentares import atualiza_parlamentares_tasks

from dags import execute_tasks_in_sequence

default_args = {
    "owner": "airflow",
    "description": "Docker atualiza_parlamentares",
    "depend_on_past": False,
    "start_date": datetime(2021, 5, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "atualiza_parlamentares",
    default_args=default_args,
    schedule_interval="0 12 * * 5",  # Update parlamentares every friday at 12:00 UTC
    catchup=False,
) as dag:
    mounts = [Mount("/agora-digital/leggo_data", "leggo_data")]

    tasks = [
        *atualiza_parlamentares_tasks(mounts)
    ]

    execute_tasks_in_sequence(tasks)
