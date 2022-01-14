from os import getenv
from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount


def r_export_tweets_to_process_task(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    t1 = DockerOperator(
        task_id="task_r_export_tweets_to_process_t1",
        # image="crawler-leggo-twitter-image",
        image="r-leggo-twitter-image",
        container_name="r_export_tweets_to_process_t1",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="leggo_twitter_network",
        mounts=mounts,
        command="""
            Rscript code/tweets/export_tweets_to_process.R
        """,
        **extraoptions,
    )

    return [t1]


def twitter_commom_dokcer_operators(env: str, mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    URL_API_PARLAMETRIA = getenv("URL_API_PARLAMETRIA")

    t1 = DockerOperator(
        task_id=f"task_process_twitter_{env}_t1",
        image="r-leggo-twitter-image",
        container_name=f"process_twitter_tasks_{env}_t1",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="leggo_twitter_network",
        mounts=mounts,
        command=f"""
            Rscript code/export_data.R -u {URL_API_PARLAMETRIA}
        """,
        **extraoptions,
    )

    t2 = DockerOperator(
        task_id=f"task_process_twitter_{env}_t2",
        image="r-leggo-twitter-image",
        container_name=f"process_twitter_tasks_{env}_t1",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="leggo_twitter_network",
        mounts=mounts,
        command=f"""
            Rscript code/processor/export_data_to_db_format.R
        """,
        **extraoptions,
    )

    return [t1, t2]


def process_twitter_tasks_development(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    return twitter_commom_dokcer_operators("development", mounts, **extraoptions)


def process_twitter_tasks_staging(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    return twitter_commom_dokcer_operators("staging", mounts, **extraoptions)


def process_twitter_tasks_production(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    return twitter_commom_dokcer_operators("production", mounts, **extraoptions)
