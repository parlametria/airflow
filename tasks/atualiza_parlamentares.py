from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def atualiza_parlamentares_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_atualiza_parlamentares",
        image="agoradigital/r-scrapper",
        container_name="atualiza_parlamentares_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/parlamentares/update_parlamentares.R \
            -p {EXPORT_FOLDERPATH}
        """,
    )

    return [t1]
