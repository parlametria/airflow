from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def processa_pls_interesse_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")
    URL_INTERESSES = getenv("URL_INTERESSES")

    t1 = DockerOperator(
        task_id="processa_pls_interesse_tasks",
        image="agoradigital/r-scrapper",
        container_name="task_processa_pls_interesse",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            Rscript scripts/interesses/export_pls_leggo.R \
                -u {URL_INTERESSES} \
                -e {EXPORT_FOLDERPATH}/pls_interesses.csv
        """,
    )

    return [t1]
