from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def build_leggo_content_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    #EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")
    #PLS_FILEPATH = getenv("PLS_FILEPATH")
    #
    #t1 = DockerOperator(
    #    task_id="task_build_leggo_content",
    #    image="agoradigital/r-scrapper",
    #    container_name="build_leggo_content_tasks",
    #    api_version="auto",
    #    auto_remove=True,
    #    docker_url="unix://var/run/docker.sock",
    #    network_mode="bridge",
    #    mounts=mounts,
    #    command=f"""
    #    curr_branch=`git -C $LEGGOCONTENT_FOLDERPATH rev-parse --abbrev-ref HEAD`
    #    git -C $LEGGOCONTENT_FOLDERPATH pull origin $curr_branch
    #
    #    docker-compose -f $LEGGOCONTENT_FOLDERPATH/docker-compose.yml build
    #    """,
    #)
    #
    #return [t1]

    return []
