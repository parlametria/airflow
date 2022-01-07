from datetime import datetime, timedelta

from airflow import DAG
from docker.types import Mount

from tasks.keep_last_backups import keep_last_backups_tasks

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
    "keep_last_backups",
    default_args=default_args,
    schedule_interval="30 7 * * *",
    catchup=False,
) as dag:
    mounts = [Mount("/agora-digital/leggo_data", "leggo_data")]

    tasks = [
        *keep_last_backups_tasks(mounts),
    ]

    execute_tasks_in_sequence(tasks)
