from typing import List
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount


def update_db_twitter_common(env: str, mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    t1 = DockerOperator(
        task_id=f"update_db_twitter_{env}_t1",
        # image="crawler-leggo-twitter-image",
        image="feed-leggo-twitter-image",
        container_name=f"update_db_twitter_{env}_t1",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="leggo_twitter_network",
        mounts=mounts,
        command="""
            python manage.py do-migrations
        """,
        **extraoptions,
    )

    t2 = DockerOperator(
        task_id=f"update_db_twitter_{env}_t2",
        # image="crawler-leggo-twitter-image",
        image="feed-leggo-twitter-image",
        container_name=f"update_db_twitter_{env}_t2",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="leggo_twitter_network",
        mounts=mounts,
        command="""
            python manage.py update-data
        """,
        **extraoptions,
    )

    return [t1, t2]


def update_db_twitter_development(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    return update_db_twitter_common("development", mounts, **extraoptions)

def update_db_twitter_production(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    return update_db_twitter_common("production", mounts, **extraoptions)


def update_table_tweets_processados(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    t1 = DockerOperator(
        task_id=f"update_table_tweets_processados_t1",
        # image="crawler-leggo-twitter-image",
        image="feed-leggo-twitter-image",
        container_name=f"update_table_tweets_processados_t1",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="leggo_twitter_network",
        mounts=mounts,
        command="""
            python manage.py update-data-tweets-processados
        """,
        **extraoptions,
    )

    return [t1]
