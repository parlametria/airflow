from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator

from docker.types import Mount

from tasks.process_votos import process_votos_tasks
from tasks.process_governismo import process_governismo_tasks
from tasks.process_orientacoes import process_orientacoes_tasks
from tasks.process_disciplina import process_disciplina_tasks
from tasks.process_votacoes_sumarizadas import process_votacoes_sumarizadas_tasks


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
    "pipeline_votacoes",
    default_args=default_args,
    schedule_interval="0 21 * * 5",
    catchup=False,
) as dag:
    start_dag = DummyOperator(task_id="start_dag")
    end_dag = DummyOperator(task_id="end_dag")
    mounts = [Mount("/agora-digital/leggo_data", "leggo_data")]

    tasks = [
        *process_votos_tasks(mounts),
        *process_governismo_tasks(mounts),
        *process_orientacoes_tasks(mounts),
        *process_disciplina_tasks(mounts),
        *process_votacoes_sumarizadas_tasks(mounts),
    ]

    current_task = start_dag
    for task in tasks:
        current_task >> task
        current_task = task

    current_task >> end_dag
