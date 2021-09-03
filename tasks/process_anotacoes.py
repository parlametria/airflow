from os import getenv
from typing import List
from airflow.operators.docker_operator import DockerOperator

from docker.types import Mount

def process_anotacoes_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")
    URL_LISTA_ANOTACOES = getenv("URL_LISTA_ANOTACOES")

    t1 = DockerOperator(
        task_id="task_process_anotacoes",
        image="agoradigital/r-scrapper",
        container_name="process_anotacoes_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            Rscript scripts/anotacoes/export_anotacoes.R \
                -u {URL_LISTA_ANOTACOES} \
                -i {EXPORT_FOLDERPATH}/pls_interesses.csv \
                -p {EXPORT_FOLDERPATH}/proposicoes.csv \
                -e {EXPORT_FOLDERPATH}
        """,
    )

    return [t1]
