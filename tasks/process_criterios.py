from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def process_criterios_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_process_criterios",
        image="agoradigital/r-scrapper",
        container_name="process_criterios_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            Rscript scripts/proposicoes/destaques/export_destaques.R \
                -p {EXPORT_FOLDERPATH}/proposicoes.csv \
                -t {EXPORT_FOLDERPATH}/progressos.csv \
                -r {EXPORT_FOLDERPATH}/trams.csv \
                -i {EXPORT_FOLDERPATH}/interesses.csv \
                -s {EXPORT_FOLDERPATH}/pressao.csv \
                -e {EXPORT_FOLDERPATH}/proposicoes_destaques.csv
        """,
    )

    return [t1]

