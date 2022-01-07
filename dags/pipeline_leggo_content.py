from datetime import datetime, timedelta

from airflow import DAG

from docker.types import Mount

from tasks.build_leggo_content import build_leggo_content_tasks
from tasks.process_leggo_content import process_leggo_content_tasks
from tasks.update_distancias_emendas import update_distancias_emendas_tasks

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
    "pipeline_leggo_content",
    default_args=default_args,
    schedule_interval="0 2 * * *",
    catchup=False,
) as dag:
    mounts = [Mount("/agora-digital/leggo_data", "leggo_data")]
    tasks_args = {'mounts': mounts, 'trigger_rule': 'all_done'}

    tasks = [
        *build_leggo_content_tasks(**tasks_args),
        *process_leggo_content_tasks(**tasks_args),
        *update_distancias_emendas_tasks(**tasks_args),
    ]

    execute_tasks_in_sequence(tasks)
