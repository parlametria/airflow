from os import getenv
from typing import List
from airflow.operators.docker_operator import DockerOperator

from docker.types import Mount

def update_distancias_emendas_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_update_distancias_emendas",
        image="agoradigital/r-scrapper",
        container_name="update_distancias_emendas_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/update_emendas_dist.R \
            {EXPORT_FOLDERPATH}/raw_emendas_distances \
            {EXPORT_FOLDERPATH}/distancias \
            {EXPORT_FOLDERPATH}/novas_emendas.csv \
            {EXPORT_FOLDERPATH}/emendas.csv
        """,
    )

    return [t1]
