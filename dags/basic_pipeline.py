from datetime import datetime, timedelta

from airflow import DAG

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

from dags import execute_tasks_in_sequence, get_agora_digital_mounts

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
    "basic_pipeline",
    default_args=default_args,
    schedule_interval="30 20 * * *",
    catchup=False,
) as dag:
    mounts = [*get_agora_digital_mounts()]
    tasks_args = {'mounts': mounts, 'trigger_rule': 'all_done'}

    tasks = [
        *setup_leggo_data_volume_tasks(**tasks_args),
        *process_entidades_tasks(**tasks_args),
        *processa_pls_interesse_tasks(**tasks_args),
        *fetch_leggo_props_tasks(**tasks_args),
        *fetch_leggo_autores_tasks(**tasks_args),
        *fetch_leggo_relatores_tasks(**tasks_args),
        *process_props_apensadas_tasks(**tasks_args),
        *process_anotacoes_tasks(**tasks_args),
        *update_leggo_data_tasks(**tasks_args),
        *process_criterios_tasks(**tasks_args),
        *process_leggo_data_tasks(**tasks_args),
    ]

    execute_tasks_in_sequence(tasks)
