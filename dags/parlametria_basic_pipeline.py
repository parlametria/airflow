from typing import Callable

from airflow.models.dag import DAG
from airflow.models import Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

import leggo_geral


def get_task_command(task_name: str) -> Callable:
    task = getattr(leggo_geral, task_name, None)

    if task is None:
        raise Exception(f"Task {task_name} could not be found")

    return task


with DAG(
    dag_id="parlametria_basic_pipeline",
    schedule_interval="@once",
    default_args={
        "owner": "airflow",
        "retries": 0,
        "retry_delay": timedelta(minutes=5),
        "start_date": datetime(2021, 8, 19, 11, 0, 0),
    },
    catchup=False,
) as dag:

    dummy_task = DummyOperator(
        task_id="dummy_task",
    )

    tasks_names = [
        "build_leggor",
        "setup_leggo_data_volume",
        "process_entidades",
        "processa_pls_interesse",
        "fetch_leggo_props",
        "fetch_leggo_autores",
        "fetch_leggo_relatores",
        "processa_interesses",
        "process_props_apensadas",
        "process_anotacoes",
        "update_leggo_data",
        "process_criterios",
        "process_leggo_data",
    ]

    tasks = []
    prev_task = dummy_task

    for task_name in tasks_names[::-1]:
        current_task_command = get_task_command(task_name)

        task = BashOperator(
            task_id=f"task_{task_name}",
            bash_command=current_task_command(),
            trigger_rule='all_done' # ignores failure and move on to next task
        )
        tasks.append(task)

        prev_task << task # Queue current_task
        prev_task = task

    # run_build_leggor >> run_process_votos  # 1º run_build_leggor
    # run_process_votos >> run_process_governismo  # 2º run_process_votos
    # run_process_governismo >> run_this_last  # 3º run_process_governismo

    # run_build_leggor >> \
    #    run_process_votos >> \
    #        run_process_governismo >> \
    #            run_this_last


if __name__ == "__main__":
    dag.cli()
