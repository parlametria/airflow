from os import getenv, path
from typing import List

from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount


def atualiza_parlamentares_tasks(
    mounts: List[Mount], **extraoptions
) -> List[DockerOperator]:
    EXPORT_CSV_FOLDERPATH = "/agora-digital/inst/extdata/"
    CSV_FILENAME = "parlamentares.csv"

    t1 = DockerOperator(
        task_id="task_atualiza_parlamentares2",
        image="airflow/atualiza_parlamentares",
        container_name="atualiza_parlamentares_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            python /atualiza_parlamentares/main.py {EXPORT_CSV_FOLDERPATH} {CSV_FILENAME}
        """,
        **extraoptions,
    )

    #    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    #t1 = DockerOperator(
    #    task_id="task_atualiza_parlamentares",
    #    image="agoradigital/r-scrapper",
    #    container_name="atualiza_parlamentares_tasks",
    #    api_version="auto",
    #    auto_remove=True,
    #    docker_url="unix://var/run/docker.sock",
    #    network_mode="bridge",
    #    mounts=mounts,
    #    command=f"""
    #    Rscript scripts/parlamentares/update_parlamentares.R \
    #        -p {EXPORT_FOLDERPATH}
    #    """,
    #    **extraoptions,
    #)

    return [t1]
