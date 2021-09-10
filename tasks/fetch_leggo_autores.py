from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def fetch_leggo_autores_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")
    PLS_FILEPATH = getenv("PLS_FILEPATH")

    t1 = DockerOperator(
        task_id="task_fetch_leggo_autores",
        image="agoradigital/r-scrapper",
        container_name="fetch_leggo_autores_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            Rscript scripts/fetch_updated_bills_data.R \
                -a {EXPORT_FOLDERPATH}/autores_leggo.csv \
                -p {PLS_FILEPATH} \
                -e {EXPORT_FOLDERPATH} \
                -f 5
        """,
    )

    return [t1]
