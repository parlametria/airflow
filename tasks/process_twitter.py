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


def process_twitter_tasks_development(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    URL_API_PARLAMETRIA = getenv("URL_API_PARLAMETRIA")

    t1 = DockerOperator(
        task_id="task_process_twitter_development_t1",
        image="r-leggo-twitter-image",
        container_name="process_twitter_tasks_development_t1",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="leggo_twitter_network",
        mounts=mounts,
        command=f"""
            Rscript code/export_data.R \
            -u {URL_API_PARLAMETRIA}
        """,
        **extraoptions,
    )

    t2 = DockerOperator(
        task_id="task_process_twitter_development_t2",
        image="r-leggo-twitter-image",
        container_name="process_twitter_tasks_development_t1",
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


def process_twitter_tasks_staging(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    URL_API_PARLAMETRIA = getenv("URL_API_PARLAMETRIA")

    t1 = DockerOperator(
        task_id="task_process_twitter_staging_t1",
        image="r-leggo-twitter-image",
        container_name="process_twitter_tasks_staging",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            Rscript code/export_data.R -u {URL_API_PARLAMETRIA}
        """,
        **extraoptions,
    )

    t2 = DockerOperator(
        task_id="task_process_twitter_staging_t2",
        image="r-leggo-twitter-image",
        container_name="process_twitter_tasks_staging",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
            Rscript code/processor/export_data_to_db_format.R
        """,
        **extraoptions,
    )

    return [t1, t2]


def process_twitter_tasks_production(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    LEGGOTWITTER_FOLDERPATH = getenv("LEGGOTWITTER_FOLDERPATH")

    t1 = DockerOperator(
        task_id="task_process_twitter_production",
        image="r-leggo-twitter-image",
        container_name="process_twitter_tasks_production",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        docker-compose -f $LEGGOTWITTER_FOLDERPATH/docker-compose.yml \
                -f $LEGGOTWITTER_FOLDERPATH/deploy/prod.yml \
                build

        docker-compose -f $LEGGOTWITTER_FOLDERPATH/docker-compose.yml \
                -f $LEGGOTWITTER_FOLDERPATH/deploy/prod.yml \
                run --rm r-twitter-service \
                Rscript code/export_data.R \
                -u $URL_API_PARLAMETRIA

        docker-compose -f $LEGGOTWITTER_FOLDERPATH/docker-compose.yml \
                -f $LEGGOTWITTER_FOLDERPATH/deploy/prod.yml \
                run --rm r-twitter-service \
                Rscript code/processor/export_data_to_db_format.R
        """,
        **extraoptions,
    )

    return [t1]
