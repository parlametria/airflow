from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash_operator import BashOperator

from docker.types import Mount


def process_new_tweets_tasks(
    mounts: List[Mount], **extraoptions
) -> List[DockerOperator]:

    t1 = DockerOperator(
        task_id="task_process_new_tweets",
        image=f"new_tweets",
        container_name="process_new_tweets_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        mount_tmp_dir=False,
        command=f"""
            python main.py --user users.txt --search search.txt
        """,
        **extraoptions,
    )

    return [t1]
