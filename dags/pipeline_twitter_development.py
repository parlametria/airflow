from datetime import datetime, timedelta
from os import getenv

from airflow import DAG

from docker.types import Mount

from tasks.process_twitter import r_export_tweets_to_process_task, process_twitter_tasks_development

from dags import execute_tasks_in_sequence

LEGGOTWITTER_FOLDERPATH = getenv("LEGGOTWITTER_FOLDERPATH")
URL_USERNAMES_TWITTER = getenv("URL_USERNAMES_TWITTER")

default_args = {
    "owner": "airflow",
    "description": "Docker process_twitter_tasks_development",
    "depend_on_past": False,
    "start_date": datetime(2021, 5, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "pipeline_twitter_development",
    default_args=default_args,
    schedule_interval=None,
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
        *process_twitter_tasks_development(**tasks_args),
    ]

    execute_tasks_in_sequence(tasks)
