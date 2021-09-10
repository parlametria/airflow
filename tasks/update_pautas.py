from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def update_pautas_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")
    PLS_FILEPATH = getenv("PLS_FILEPATH")


    t1 = DockerOperator(
        task_id="task_update_pautas",
        image="agoradigital/r-scrapper",
        container_name="update_pautas_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/fetch_agenda.R \
          {PLS_FILEPATH} \
          $lastweek $today \
          {EXPORT_FOLDERPATH} \
          {EXPORT_FOLDERPATH}/pautas.csv
        """,
    )

    return [t1]
