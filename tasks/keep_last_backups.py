from os import getenv
from typing import List
from airflow.operators.docker_operator import DockerOperator

from docker.types import Mount

def keep_last_backups_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    BACKUP_FOLDERPATH = getenv("BACKUP_FOLDERPATH")
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    backups_to_keep = 8 # it was 7 + 1 on the orignal script

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
        ls -lt {EXPORT_FOLDERPATH}/backups | grep ^d | tail -n {backups_to_keep} | awk """ + "'{print $9}'" + f""" | while IFS= read -r f; do
                echo 'Removendo backups'
                rm -rf {EXPORT_FOLDERPATH}/backups
        done
        """,
    )

    return [t1]
