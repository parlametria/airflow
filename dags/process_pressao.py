from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

from docker.types import Mount

from tasks.process_pressao import process_pressao_tasks

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
    start_dag = DummyOperator(task_id="start_dag")
    end_dag = DummyOperator(task_id="end_dag")
    mounts = [Mount("/leggo-trends/leggo_data", "leggo_data")]

    tasks = [
        *process_pressao_tasks(mounts)
    ]

    current_task = start_dag
    for task in tasks:
        current_task >> task
        current_task = task

    current_task >> end_dag
