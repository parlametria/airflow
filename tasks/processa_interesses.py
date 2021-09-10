from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def processa_interesses_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")
    URL_INTERESSES = getenv("URL_INTERESSES")

    t1 = DockerOperator(
        task_id="task_processa_interesses",
        image="agoradigital/r-scrapper",
        container_name="processa_interesses_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            Rscript scripts/interesses/export_mapeamento_interesses.R \
                -u {URL_INTERESSES} \
                -p {EXPORT_FOLDERPATH}/proposicoes.csv \
                -e {EXPORT_FOLDERPATH}/interesses.csv
        """,
    )

    return [t1]
