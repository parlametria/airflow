from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

## DEPRECATED
#  leggo-geral/README.md
# 37:- [leggo-content](https://github.com/parlametria/leggo-content) (deprecated)
def process_leggo_content_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    #LEGGOCONTENT_FOLDERPATH = getenv("LEGGOCONTENT_FOLDERPATH")
    #
    #t1 = DockerOperator(
    #    task_id="task_process_leggo_content",
    #    image="agoradigital/r-scrapper",
    #    container_name="process_leggo_content_tasks",
    #    api_version="auto",
    #    auto_remove=True,
    #    docker_url="unix://var/run/docker.sock",
    #    network_mode="bridge",
    #    mounts=mounts,
    #    command=f"""
    #        docker-compose -f {LEGGOCONTENT_FOLDERPATH}/docker-compose.yml run \
    #            --rm leggo-content \
    #            ./run_emendas_analysis.sh \
    #            ./leggo_content_data \
    #            ./leggo_data
    #    """,
    #)

    #return [t1]
    return []
