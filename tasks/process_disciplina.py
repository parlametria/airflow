from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def process_disciplina_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_process_disciplina",
        image="agoradigital/r-scrapper",
        container_name="process_disciplina_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/disciplina/export_disciplina.R \
            -v {EXPORT_FOLDERPATH}/votos.csv \
            -o {EXPORT_FOLDERPATH}/orientacoes.csv \
            -p {EXPORT_FOLDERPATH}/votacoes.csv \
            -i "2019-02-01" \
            -f "2022-12-31" \
            -e {EXPORT_FOLDERPATH}/disciplina.csv
        """,
    )

    return [t1]
