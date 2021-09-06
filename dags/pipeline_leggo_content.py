from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

from docker.types import Mount

from tasks.build_leggo_content import build_leggo_content_tasks
from tasks.process_leggo_content import process_leggo_content_tasks
from tasks.update_distancias_emendas import update_distancias_emendas_tasks


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
    "pipeline_leggo_content",
    default_args=default_args,
    schedule_interval="0 2 * * *",
    catchup=False,
) as dag:
    start_dag = DummyOperator(task_id="start_dag")
    end_dag = DummyOperator(task_id="end_dag")
    mounts = [Mount("/agora-digital/leggo_data", "leggo_data")]

    tasks = [
        *build_leggo_content_tasks(mounts),
        *process_leggo_content_tasks(mounts),
        *update_distancias_emendas_tasks(mounts),
    ]

    current_task = start_dag
    for task in tasks:
        current_task >> task
        current_task = task

    current_task >> end_dag
