from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def process_votos_tasks(mounts: List[Mount],**extraoptions) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_process_votos",
        image="agoradigital/r-scrapper",
        container_name="process_votos_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/votos/export_votos.R \
            -v {EXPORT_FOLDERPATH}/votacoes.csv \
            -u {EXPORT_FOLDERPATH}/votos.csv \
            -p {EXPORT_FOLDERPATH}/proposicoes.csv \
            -e {EXPORT_FOLDERPATH}/entidades.csv
        """,
        **extraoptions,
    )

    return [t1]
