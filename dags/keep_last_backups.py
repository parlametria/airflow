from airflow.models.dag import DAG
from datetime import datetime, timedelta

from leggo_scripts.util import linear_task_queue


with DAG(
    dag_id="keep_last_backups",
    schedule_interval="30 7 * * *", # Generate backup Leggo data 7:30 UTC
    default_args={
        "owner": "airflow",
        "retries": 0,
        "retry_delay": timedelta(minutes=5),
        "start_date": datetime(2021, 8, 19, 11, 0, 0),
    },
    catchup=False,
) as dag:
    tasks_names = [
        "keep_last_backups",
    ]

    linear_task_queue(tasks_names)


if __name__ == "__main__":
    dag.cli()
