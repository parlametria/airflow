from airflow.models.dag import DAG
from datetime import datetime, timedelta

from leggo_scripts.util import linear_task_queue


""" with DAG(
    dag_id="pipeline_leggo_content",
    schedule_interval="0 2 * * *", # Run Leggo emendas pipeline every day (fetch, analyze)
    default_args={
        "owner": "airflow",
        "retries": 0,
        "retry_delay": timedelta(minutes=5),
        "start_date": datetime(2021, 8, 19, 11, 0, 0),
    },
    catchup=False,
) as dag:
    tasks_names = [
        "build_leggo_content",
        "process_leggo_content",
        "update_distancias_emendas",
    ]

    linear_task_queue(tasks_names)


if __name__ == "__main__":
    dag.cli() """
