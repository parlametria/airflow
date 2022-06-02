from datetime import datetime, timedelta
from airflow import DAG
from tasks.process_new_tweets.process_new_tweets import process_new_tweets_tasks
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
    schedule_interval=None,  # Run tweets fetcher 22:00 UTC
    catchup=False,
) as dag:

    tasks = [*process_new_tweets_tasks()]

    execute_tasks_in_sequence(tasks)
