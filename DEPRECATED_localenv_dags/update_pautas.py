from airflow.models.dag import DAG
from datetime import datetime, timedelta

from leggo_scripts.util import linear_task_queue


with DAG(
    dag_id="update_pautas",
    schedule_interval="30 11 * * 1-5", # Update pautas every weekday morning
    default_args={
        "owner": "airflow",
        "retries": 0,
        "retry_delay": timedelta(minutes=5),
        "start_date": datetime(2021, 8, 19, 11, 0, 0),
    },
    catchup=False,
) as dag:
    tasks_names = [
        "update_pautas",
    ]

    linear_task_queue(tasks_names)


if __name__ == "__main__":
    dag.cli()
