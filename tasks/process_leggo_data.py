from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def process_leggo_data_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_process_leggo_data",
        image="agoradigital/r-scrapper",
        container_name="process_leggo_data_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/process_leggo_data.R \
            -f 1 \
            -d "2019-01-31" \
            -p 0.1 \
            -i {EXPORT_FOLDERPATH} \
            -o {EXPORT_FOLDERPATH} \
            -e {EXPORT_FOLDERPATH}/entidades.csv
        """,
    )

    return [t1]
