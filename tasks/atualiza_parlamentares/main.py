from os import getenv
from typing import List

from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.python_operator import PythonOperator

from docker.types import Mount

from tasks.atualiza_parlamentares.process_parlamentares import update_parlamentares


def atualiza_parlamentares_tasks(
    mounts: List[Mount], **extraoptions
) -> List[DockerOperator]:
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_atualiza_parlamentares",
        image="agoradigital/r-scrapper",
        container_name="atualiza_parlamentares_tasks",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/parlamentares/update_parlamentares.R \
            -p {EXPORT_FOLDERPATH}
        """,
        **extraoptions,
    )

    return [t1]


#kwargs = {
#    "mounts": [
#        {
#            "Target": "/agora-digital/leggo_data",
#            "Source": "leggo_data",
#            "Type": "volume",
#            "ReadOnly": False,
#        },
#        {
#            "Target": "/agora-digital/scripts",
#            "Source": "/home/fabio/Pencil/parlametria/leggoR/scripts",
#            "Type": "bind",
#            "ReadOnly": False,
#        },
#        {
#            "Target": "/agora-digital/inst",
#            "Source": "/home/fabio/Pencil/parlametria/leggoR/inst",
#            "Type": "bind",
#            "ReadOnly": False,
#        },
#    ]
#}


def atualiza_parlamentares_tasks2(
    mounts: List[Mount], **extraoptions
) -> List[PythonOperator]:

    # /agora-digital/inst/parlamentares.csv
    def settup_update_parlamentares(FILE_PATH: str, **kwargs):
        update_parlamentares(FILE_PATH)

    t1 = PythonOperator(
        task_id="task_atualiza_parlamentares2",
        python_callable=settup_update_parlamentares,
        mounts=mounts,
        op_kwargs={
            "FILE_PATH": "/agora-digital/inst/extdata/parlamentares.csv",
        },
    )

    return [t1]
