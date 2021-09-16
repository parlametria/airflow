from datetime import datetime, timedelta
from os import getenv

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

from docker.types import Mount

from tasks.process_twitter import process_twitter_tasks_development

LEGGOTWITTER_DADOS_FOLDERPATH = getenv("LEGGOTWITTER_DADOS_FOLDERPATH")

default_args = {
    "owner": "airflow",
    "description": "Docker process_twitter_tasks_development",
    "depend_on_past": False,
    "start_date": datetime(2021, 5, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "pipeline_twitter_development",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:
    start_dag = DummyOperator(task_id="start_dag")
    end_dag = DummyOperator(task_id="end_dag")
    mounts = [
        Mount("/leggo-twitter-dados/data", "leggo_twitter_dados_data"), # /data:/leggo-twitter-dados/data
    ]

    tasks = [
        *process_twitter_tasks_development(mounts),
    ]

    current_task = start_dag
    for task in tasks:
        current_task >> task
        current_task = task

    current_task >> end_dag
