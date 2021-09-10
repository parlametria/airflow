from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def process_props_apensadas_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_process_props_apensadas",
        image="agoradigital/r-scrapper",
        container_name="process_props_apensadas_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/proposicoes/apensadas/export_apensadas.R \
            -p {EXPORT_FOLDERPATH}/proposicoes.csv \
            -i {EXPORT_FOLDERPATH}/interesses.csv \
            -o {EXPORT_FOLDERPATH}
        """,
    )

    return [t1]
