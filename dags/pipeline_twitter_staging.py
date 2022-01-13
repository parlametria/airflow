from os import getenv
from datetime import datetime, timedelta

from airflow import DAG

from docker.types import Mount

from tasks.process_twitter import process_twitter_tasks_staging, r_export_tweets_to_process_task

from dags import execute_tasks_in_sequence

LEGGOTWITTER_FOLDERPATH = getenv("LEGGOTWITTER_FOLDERPATH")
URL_USERNAMES_TWITTER = getenv("URL_USERNAMES_TWITTER")

default_args = {
    "owner": "airflow",
    "description": "Docker process_twitter_tasks_staging",
    "depend_on_past": False,
    "start_date": datetime(2021, 5, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "pipeline_twitter_staging",
    default_args=default_args,
    schedule_interval="0 5 * * *",  # Run twitter pipeline staging 5:00 UTC
    catchup=False,
) as dag:
    mounts = [
        # /data:/leggo-twitter-dados/data
        Mount("/leggo-twitter-dados/data", f"{LEGGOTWITTER_FOLDERPATH}/data", type="bind"),
    ]

    tasks_args = {
        'mounts': mounts,
        'trigger_rule': 'all_done',
        'environment': {
            'URL_USERNAMES_TWITTER': URL_USERNAMES_TWITTER
        }
    }

    tasks = [
        *r_export_tweets_to_process_task(**tasks_args),
        *process_twitter_tasks_staging(**tasks_args),
    ]

    execute_tasks_in_sequence(tasks)
