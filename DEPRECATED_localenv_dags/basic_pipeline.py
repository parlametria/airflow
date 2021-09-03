from airflow.models.dag import DAG
from datetime import datetime, timedelta

from leggo_scripts.util import linear_task_queue


with DAG(
    dag_id="basic_pipeline",
    schedule_interval="30 20 * * *",  # Run leggo basic pipeline every day 20:30 UTC
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

    linear_task_queue(tasks_names)

if __name__ == "__main__":
    dag.cli()
