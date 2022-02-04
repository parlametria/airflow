from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def process_tweets_tasks(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    # LEGGOTWITTER_FOLDERPATH = getenv("LEGGOTWITTER_FOLDERPATH")
    URL_USERNAMES_TWITTER = getenv("URL_USERNAMES_TWITTER")

    t1 = DockerOperator(
        task_id="task_process_tweets",
        #image="agoradigital/r-scrapper",
        #image="feed-leggo-twitter-image",
        image="crawler-leggo-twitter-image",
        container_name="process_tweets_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        # network_mode="bridge",
        network_mode="leggo_twitter_network",
        mounts=mounts,
        command=f"""
            python manage.py process-tweets -l \"{URL_USERNAMES_TWITTER}\"
        """,
       **extraoptions,
    )

    return [t1]
