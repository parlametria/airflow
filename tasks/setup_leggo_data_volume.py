from os import getenv
from typing import List
from airflow.operators.docker_operator import DockerOperator

from docker.types import Mount


def setup_leggo_data_volume_tasks(mounts: List[Mount]) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="copy_props_tables_to_volume",
        image="agoradigital/r-scrapper",
        container_name="task_rmod_copy_props_tables_to_volume",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            cp inst/extdata/tabela_geral_ids_casa.csv \
                inst/extdata/tabela_geral_ids_casa_new.csv \
                {EXPORT_FOLDERPATH}
        """,
    )

    t2 = DockerOperator(
        task_id="create_folders_for_docs_data",
        image="agoradigital/r-scrapper",
        container_name="task_rmod_create_folders_for_docs_data",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            mkdir -p {EXPORT_FOLDERPATH}/camara \
                        {EXPORT_FOLDERPATH}/senado
        """,
    )

    t3 = DockerOperator(
        task_id="copy_deputados_data_to_their_respective_folder",
        image="agoradigital/r-scrapper",
        container_name="task_rmod_copy_deputados_data_to_their_respective_folder",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            cp inst/extdata/camara/parlamentares.csv \
                {EXPORT_FOLDERPATH}/camara/parlamentares.csv
        """,
    )

    t4 = DockerOperator(
        task_id="copy_senadores_data_to_their_respective_folder",
        image="agoradigital/r-scrapper",
        container_name="task_rmod_copy_senadores_data_to_their_respective_folder",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            cp inst/extdata/senado/parlamentares.csv \
                {EXPORT_FOLDERPATH}/senado/parlamentares.csv
        """,
    )

    t5 = DockerOperator(
        task_id="copy_parliamentarians_data_to_their_respective_folder",
        image="agoradigital/r-scrapper",
        container_name="task_rmod_copy_parliamentarians_data_to_their_respective_folder",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            cp inst/extdata/parlamentares.csv \
                {EXPORT_FOLDERPATH}/parlamentares.csv
        """,
    )

    return [t1, t2, t3, t4, t5]
