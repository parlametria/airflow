from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def process_governismo_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_process_governismo",
        image="agoradigital/r-scrapper",
        container_name="process_governismo_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/governismo/export_governismo.R \
            -v {EXPORT_FOLDERPATH}/votos.csv \
            -p {EXPORT_FOLDERPATH}/votacoes.csv \
            -i "2019-02-01" \
            -f "2022-12-31" \
            -e {EXPORT_FOLDERPATH}/governismo.csv
        """,
    )

    return [t1]
