from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def process_entidades_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="process_entidades_tasks",
        image="agoradigital/r-scrapper",
        container_name="task_process_entidades",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            Rscript scripts/entidades/export_entidades.R \
                -p {EXPORT_FOLDERPATH}/parlamentares.csv \
                -o {EXPORT_FOLDERPATH}
        """,
    )

    return [t1]
