from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

from docker.types import Mount

from tasks.setup_leggo_data_volume import setup_leggo_data_volume_tasks
from tasks.process_entidades import process_entidades_tasks
from tasks.processa_pls_interesse import processa_pls_interesse_tasks
from tasks.fetch_leggo_props import fetch_leggo_props_tasks
from tasks.fetch_leggo_autores import fetch_leggo_autores_tasks
from tasks.fetch_leggo_relatores import fetch_leggo_relatores_tasks
from tasks.process_props_apensadas import process_props_apensadas_tasks
from tasks.process_anotacoes import process_anotacoes_tasks
from tasks.update_leggo_data import update_leggo_data_tasks
from tasks.process_criterios import process_criterios_tasks
from tasks.process_leggo_data import process_leggo_data_tasks

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
    "docker_basic_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:
    start_dag = DummyOperator(task_id="start_dag")
    end_dag = DummyOperator(task_id="end_dag")
    mounts = [Mount("/agora-digital/leggo_data", "leggo_data")]

    tasks = [
        *setup_leggo_data_volume_tasks(mounts),
        *process_entidades_tasks(mounts),
        *processa_pls_interesse_tasks(mounts),
        *fetch_leggo_props_tasks(mounts),
        *fetch_leggo_autores_tasks(mounts),
        *fetch_leggo_relatores_tasks(mounts),
        *process_props_apensadas_tasks(mounts),
        *process_anotacoes_tasks(mounts),
        *update_leggo_data_tasks(mounts),
        *process_criterios_tasks(mounts),
        *process_leggo_data_tasks(mounts),
    ]

    current_task = start_dag
    for task in tasks:
        current_task >> task
        current_task = task

    current_task >> end_dag
