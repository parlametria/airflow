from os import getcwd
from dotenv import dotenv_values

CURRENT_DIR = getcwd()
PARLAMETRIA_DIR = CURRENT_DIR.replace("/airflow_parlametria", "/")
LEGGO_GERAL_ENV_VARS = dotenv_values(f"{PARLAMETRIA_DIR}leggo-geral/.env")


def getvar(varname: str) -> str:
    """
    Get env variable from leggo-geral
    """
    value = LEGGO_GERAL_ENV_VARS[varname]

    if varname == "LEGGOR_FOLDERPATH":
        return "".join([PARLAMETRIA_DIR, value.replace("./", "")])

    return value


# Build do leggoR
def build_leggor():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")

    return f"""
    curr_branch=`git -C {LEGGOR_FOLDERPATH}/rcongresso rev-parse --abbrev-ref HEAD`
    git -C {LEGGOR_FOLDERPATH}/rcongresso pull origin $curr_branch

    curr_branch=`git -C {LEGGOR_FOLDERPATH} rev-parse --abbrev-ref HEAD`
    git -C {LEGGOR_FOLDERPATH} pull origin $curr_branch

    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml build --build-arg clone_rcongresso=false rmod
    """


# Processa dados de votações e votos na legislatura atual
def process_votos():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")

    return f"""
    echo "Atualiza e processa dados de votos"
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/votos/export_votos.R \
       -v {EXPORT_FOLDERPATH}/votacoes.csv \
       -u {EXPORT_FOLDERPATH}/votos.csv \
       -p {EXPORT_FOLDERPATH}/proposicoes.csv \
       -e {EXPORT_FOLDERPATH}/entidades.csv
    """


# Calcula o governismo com base nos votos nominais dos parlamentares
def process_governismo():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")

    return f"""
    echo "Processando dados de Governismo"
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
        Rscript scripts/governismo/export_governismo.R \
        -v {EXPORT_FOLDERPATH}/votos.csv \
        -p {EXPORT_FOLDERPATH}/votacoes.csv \
        -i "2019-02-01" \
        -f "2022-12-31" \
        -e {EXPORT_FOLDERPATH}/governismo.csv
    """


def setup_leggo_data_volume():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")

    return f"""
    # Copy props tables to volume
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
    cp inst/extdata/tabela_geral_ids_casa.csv inst/extdata/tabela_geral_ids_casa_new.csv \
    {EXPORT_FOLDERPATH}

    # Create folders for docs data
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
    mkdir -p {EXPORT_FOLDERPATH}/camara \
    {EXPORT_FOLDERPATH}/senado

    # Copy deputados data to their respective folder
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
    cp inst/extdata/camara/parlamentares.csv \
    {EXPORT_FOLDERPATH}/camara/parlamentares.csv

    # Copy senadores data to their respective folder
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
    cp inst/extdata/senado/parlamentares.csv \
    {EXPORT_FOLDERPATH}/senado/parlamentares.csv

    # Copy parliamentarians data to their respective folder
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
    cp inst/extdata/parlamentares.csv \
    {EXPORT_FOLDERPATH}/parlamentares.csv
    """


def process_entidades():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
        Rscript scripts/entidades/export_entidades.R \
        -p {EXPORT_FOLDERPATH}/parlamentares.csv \
        -o {EXPORT_FOLDERPATH}
    """


def processa_pls_interesse():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")
    URL_INTERESSES = getvar("URL_INTERESSES")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
        Rscript scripts/interesses/export_pls_leggo.R \
        -u {URL_INTERESSES} \
        -e {EXPORT_FOLDERPATH}/pls_interesses.csv
    """


def fetch_leggo_props():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")
    PLS_FILEPATH = getvar("PLS_FILEPATH")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/fetch_updated_bills_data.R \
       -p {PLS_FILEPATH} \
       -e {EXPORT_FOLDERPATH} \
       -f 2
    """


def fetch_leggo_autores():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")
    PLS_FILEPATH = getvar("PLS_FILEPATH")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
        Rscript scripts/fetch_updated_bills_data.R \
        -a {EXPORT_FOLDERPATH}/autores_leggo.csv \
        -p {PLS_FILEPATH} \
        -e {EXPORT_FOLDERPATH} \
        -f 5
    """


def fetch_leggo_relatores():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")
    PLS_FILEPATH = getvar("PLS_FILEPATH")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/fetch_updated_bills_data.R \
       -p {PLS_FILEPATH} \
       -o {EXPORT_FOLDERPATH}/proposicoes.csv \
       -e {EXPORT_FOLDERPATH} \
       -f 6
    """


def processa_interesses():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")
    URL_INTERESSES = getvar("URL_INTERESSES")

    return f"""
    echo "==============================="
    echo "Processa o mapeamento de pls e interesses"
    echo "==============================="
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/interesses/export_mapeamento_interesses.R \
       -u {URL_INTERESSES} \
       -p {EXPORT_FOLDERPATH}/proposicoes.csv \
       -e {EXPORT_FOLDERPATH}/interesses.csv
    """


def process_props_apensadas():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/proposicoes/apensadas/export_apensadas.R \
       -p {EXPORT_FOLDERPATH}/proposicoes.csv \
       -i {EXPORT_FOLDERPATH}/interesses.csv \
       -o {EXPORT_FOLDERPATH}
    """


def process_anotacoes():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")
    URL_LISTA_ANOTACOES = getvar("URL_LISTA_ANOTACOES")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/anotacoes/export_anotacoes.R \
       -u {URL_LISTA_ANOTACOES} \
       -i {EXPORT_FOLDERPATH}/pls_interesses.csv \
       -p {EXPORT_FOLDERPATH}/proposicoes.csv \
       -e {EXPORT_FOLDERPATH}
    """


def update_leggo_data():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")
    PLS_FILEPATH = getvar("PLS_FILEPATH")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/update_leggo_data.R \
       -p {PLS_FILEPATH} \
       -e {EXPORT_FOLDERPATH} -c camara

    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/update_leggo_data.R \
       -p {PLS_FILEPATH} \
       -e {EXPORT_FOLDERPATH} -c senado
    """


def process_criterios():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/proposicoes/destaques/export_destaques.R \
       -p {EXPORT_FOLDERPATH}/proposicoes.csv \
       -t {EXPORT_FOLDERPATH}/progressos.csv \
       -r {EXPORT_FOLDERPATH}/trams.csv \
       -i {EXPORT_FOLDERPATH}/interesses.csv \
       -s {EXPORT_FOLDERPATH}/pressao.csv \
       -e {EXPORT_FOLDERPATH}/proposicoes_destaques.csv
    """


# TODO: Why there is fixed date in the script ? "2019-01-31"
def process_leggo_data():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/process_leggo_data.R \
       -f 1 \
       -d "2019-01-31" \
       -p 0.1 \
       -i {EXPORT_FOLDERPATH} \
       -o {EXPORT_FOLDERPATH} \
       -e {EXPORT_FOLDERPATH}/entidades.csv
    """


def process_orientacoes():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/orientacoes/export_orientacoes.R \
       -v {EXPORT_FOLDERPATH}/votacoes.csv \
       -u {EXPORT_FOLDERPATH}/votos.csv \
       -o {EXPORT_FOLDERPATH}/orientacoes.csv
    """

# TODO: Why there is fixed date in the script ? "2019-02-01" and "2022-12-31"
def process_disciplina():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/disciplina/export_disciplina.R \
       -v {EXPORT_FOLDERPATH}/votos.csv \
       -o {EXPORT_FOLDERPATH}/orientacoes.csv \
       -p {EXPORT_FOLDERPATH}/votacoes.csv \
       -i "2019-02-01" \
       -f "2022-12-31" \
       -e {EXPORT_FOLDERPATH}/disciplina.csv
    """


def process_votacoes_sumarizadas():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")

    return f"""
    docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
       Rscript scripts/votacoes_sumarizadas/export_votacoes_sumarizadas.R \
       -v {EXPORT_FOLDERPATH}/votos.csv \
       -o {EXPORT_FOLDERPATH}/orientacoes.csv \
       -p {EXPORT_FOLDERPATH}/votacoes.csv \
       -i "2019-02-01" \
       -f "2022-12-31" \
       -e {EXPORT_FOLDERPATH}/votacoes_sumarizadas.csv
    """

def update_pautas():
    LEGGOR_FOLDERPATH = getvar("LEGGOR_FOLDERPATH")
    PLS_FILEPATH = getvar("PLS_FILEPATH")
    EXPORT_FOLDERPATH = getvar("EXPORT_FOLDERPATH")

    return f"""
        today=$(date +%Y-%m-%d)
        lastweek=$(date -d '2 weeks ago' +%Y-%m-%d)
        docker-compose -f {LEGGOR_FOLDERPATH}/docker-compose.yml run --rm rmod \
          Rscript scripts/fetch_agenda.R \
          {PLS_FILEPATH} \
          $lastweek $today \
          {EXPORT_FOLDERPATH} \
          {EXPORT_FOLDERPATH}/pautas.csv
    """

def keep_last_backups():
    BACKUP_FOLDERPATH = getvar("BACKUP_FOLDERPATH")

    return """
    echo "=========================================="
    echo "Mantendo apenas os últimos backups gerados"
    echo "=========================================="

    backups_to_keep=7
    ls -lt """ + BACKUP_FOLDERPATH + """ | grep ^d | tail -n +$(($backups_to_keep + 1)) | awk '{print $9}' | while IFS= read -r f; do
        echo "Removendo """ + BACKUP_FOLDERPATH + """
        rm -rf """ + BACKUP_FOLDERPATH + """
    done
    """
