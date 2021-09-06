from os import getenv
from typing import List
from airflow.operators.docker_operator import DockerOperator

from docker.types import Mount

def process_votacoes_sumarizadas_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_process_votacoes_sumarizadas",
        image="agoradigital/r-scrapper",
        container_name="process_votacoes_sumarizadas_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/votacoes_sumarizadas/export_votacoes_sumarizadas.R \
            -v {EXPORT_FOLDERPATH}/votos.csv \
            -o {EXPORT_FOLDERPATH}/orientacoes.csv \
            -p {EXPORT_FOLDERPATH}/votacoes.csv \
            -i "2019-02-01" \
            -f "2022-12-31" \
            -e {EXPORT_FOLDERPATH}/votacoes_sumarizadas.csv
        """,
    )

    return [t1]
