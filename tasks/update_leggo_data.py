from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def update_leggo_data_tasks(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")
    PLS_FILEPATH = getenv("PLS_FILEPATH")

    t1 = DockerOperator(
        task_id="task_1_update_leggo_data",
        image="agoradigital/r-scrapper",
        container_name="update_leggo_data_tasks_1",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            Rscript scripts/update_leggo_data.R \
                -p {PLS_FILEPATH} \
                -e {EXPORT_FOLDERPATH} -c camara
        """,
        **extraoptions,
    )

    t2 = DockerOperator(
        task_id="task_2_update_leggo_data",
        image="agoradigital/r-scrapper",
        container_name="update_leggo_data_tasks_2",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            Rscript scripts/update_leggo_data.R \
                -p {PLS_FILEPATH} \
                -e {EXPORT_FOLDERPATH} -c senado
        """,
        **extraoptions,
    )

    return [t1, t2]
