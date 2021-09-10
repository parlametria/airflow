from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def process_tweets_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    LEGGOTWITTER_FOLDERPATH = getenv("LEGGOTWITTER_FOLDERPATH")
    URL_USERNAMES_TWITTER = getenv("URL_USERNAMES_TWITTER")

    t1 = DockerOperator(
        task_id="task_process_tweets",
        image="agoradigital/r-scrapper",
        container_name="process_tweets_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
       docker-compose -f {LEGGOTWITTER_FOLDERPATH}/docker-compose.yml \
       -f {LEGGOTWITTER_FOLDERPATH}/docker-compose.override.yml \
       run --no-deps --rm crawler-twitter-service \
       sh -c "python manage.py process-tweets -l '""" + URL_USERNAMES_TWITTER + "\"'",
    )

    return [t1]
