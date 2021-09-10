from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def process_orientacoes_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_process_orientacoes",
        image="agoradigital/r-scrapper",
        container_name="process_orientacoes_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/orientacoes/export_orientacoes.R \
            -v {EXPORT_FOLDERPATH}/votacoes.csv \
            -u {EXPORT_FOLDERPATH}/votos.csv \
            -o {EXPORT_FOLDERPATH}/orientacoes.csv
        """,
    )

    return [t1]
