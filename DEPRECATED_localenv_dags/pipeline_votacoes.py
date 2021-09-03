from airflow.models.dag import DAG
from datetime import datetime, timedelta

from leggo_scripts.util import linear_task_queue


with DAG(
    dag_id="pipeline_votacoes",
    schedule_interval="0 21 * * 5", # Run votacoes pipeline every friday 21:00 UTC
    default_args={
        "owner": "airflow",
        "retries": 0,
        "retry_delay": timedelta(minutes=5),
        "start_date": datetime(2021, 8, 19, 11, 0, 0),
    },
    catchup=False,
) as dag:
    tasks_names = [
        "build_leggor",
        "process_votos",
        "process_governismo",
        "process_orientacoes",
        "process_disciplina",
        "process_votacoes_sumarizadas",
    ]

    linear_task_queue(tasks_names)


if __name__ == "__main__":
    dag.cli()
