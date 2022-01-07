from os import getenv
from typing import List
from datetime import datetime
from dateutil.relativedelta import relativedelta
from airflow.providers.docker.operators.docker import DockerOperator

from docker.types import Mount

def process_pressao_tasks(mounts: List[Mount], **extraoptions) -> List[DockerOperator]:
    #build_leggo_trends() {
    #    curr_branch=`git -C $LEGGOTRENDS_FOLDERPATH rev-parse --abbrev-ref HEAD`
    #    git -C $LEGGOTRENDS_FOLDERPATH pull origin $curr_branch
    #
    #    pprint "Atualizando imagem docker"
    #    docker-compose -f $LEGGOTRENDS_FOLDERPATH/docker-compose.yml build
    #    check_errs $? "Não foi possível fazer o build do leggoTrends."
    #}
    URL_TWITTER_API = getenv("URL_TWITTER_API")
    EXPORT_FOLDERPATH = getenv("EXPORT_FOLDERPATH")

    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    three_monthsago = (now - relativedelta(months=3)).strftime("%Y-%m-%d")

    t1 = DockerOperator(
        task_id="task_build_leggo_trends_t1",
        image="agoradigital/leggo-trends",
        container_name="build_leggo_trends_task",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/tweets/export_tweets.R \
            -u {URL_TWITTER_API}/proposicoes \
            -i {three_monthsago} \
            -f {today} \
            -o {EXPORT_FOLDERPATH}/tweets_proposicoes.csv
        """,
        **extraoptions,
    )

    t2 = DockerOperator(
        task_id="task_build_leggo_trends_t2",
        image="agoradigital/leggo-trends",
        container_name="build_leggo_trends_task",
        api_version="auto",
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=mounts,
        command=f"""
        Rscript scripts/popularity/export_popularity.R \
            -t {EXPORT_FOLDERPATH}/tweets_proposicoes.csv \
            -g {EXPORT_FOLDERPATH}/pops \
            -i {EXPORT_FOLDERPATH}/interesses.csv \
            -p {EXPORT_FOLDERPATH}/proposicoes.csv \
            -o {EXPORT_FOLDERPATH}/pressao.csv
        """,
        **extraoptions,
    )

    return [t1, t2]
