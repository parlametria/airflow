from datetime import datetime, timedelta
from os import getenv
from dotenv import dotenv_values

from airflow import DAG

from docker.types import Mount

from tasks.process_new_tweets import process_new_tweets_tasks
from dags import execute_tasks_in_sequence

default_args = {
    "owner": "airflow",
    "description": "Docker process_new_tweets",
    "depend_on_past": False,
    "start_date": datetime(2021, 5, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "process_new_tweets",
    default_args=default_args,
    schedule_interval="0 22 * * *",  # Run tweets fetcher 22:00 UTC
    catchup=False,
) as dag:
    twitter_credentials = dotenv_values(f"/airflow/.env.twitter-crentials")

    mounts = [
        # Mount("/agora-digital/leggo_data", "leggo_data"),
        Mount(f"./tasks/tweets/", f"./tasks/tweets", type="bind"),
    ]

    tasks_args = {
        "mounts": mounts,
        "trigger_rule": "all_done",
        "environment": {
            "TWITTER_CREDENTIALS": twitter_credentials,
        },
    }

    tasks = [*process_new_tweets_tasks(**tasks_args)]

    execute_tasks_in_sequence(tasks)
