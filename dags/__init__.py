from typing import List
from os import getenv

from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

LEGGO_HOME_FOLDERPATH = getenv("LEGGO_HOME_FOLDERPATH")


def execute_tasks_in_sequence(tasks: List[DockerOperator]):
    start_dag = DummyOperator(task_id="start_dag")
    end_dag = DummyOperator(task_id="end_dag")

    current_task = start_dag
    for task in tasks:
        current_task >> task
        current_task = task

    current_task >> end_dag


def get_agora_digital_mounts() -> List[Mount]:
    return [
        Mount("/agora-digital/leggo_data", "leggo_data"),
        Mount(
            "/agora-digital/scripts",
            f"{LEGGO_HOME_FOLDERPATH}/leggoR/scripts",
            type="bind",
        ),
        Mount(
            "/agora-digital/inst",
            f"{LEGGO_HOME_FOLDERPATH}/leggoR/inst",
            type="bind"
        ),
    ]
