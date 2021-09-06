from os import getenv
from typing import List
from airflow.operators.docker_operator import DockerOperator

from docker.types import Mount

def keep_last_backups_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    BACKUP_FOLDERPATH = getenv("BACKUP_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_keep_last_backups",
        image="agoradigital/r-scrapper",
        container_name="keep_last_backups_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        backups_to_keep=7
        ls -lt {BACKUP_FOLDERPATH} \
            | grep ^d \
            | tail -n +$(($backups_to_keep + 1)) \
            | awk """ + "'{print $9}'" + f""" \
            | while IFS= read -r f; do \
                echo 'Removendo ' {BACKUP_FOLDERPATH} \
                rm -rf {BACKUP_FOLDERPATH}
        """,
    )

    return [t1]
