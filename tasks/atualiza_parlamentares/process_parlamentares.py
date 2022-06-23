import csv
import requests
import json

from typing import Iterable, Tuple

from tasks.atualiza_parlamentares.fetch_deputados import fetch_deputados


CAMARA = "camara"
SENADO = "senado"
DEPUTADOS_PATH = "/api/v2/deputados"
CAMARA_API_LINK = "https://dadosabertos.camara.leg.br"
SENADO_API_LINK = "https://legis.senado.leg.br"


def format_deputado_data(deputado):
    deputado['nome_civil'] = deputado['nome_civil'].title()
    return deputado

def process_deputados(legs: Tuple[str]):
    deputados = fetch_deputados(legs)
    print(deputados)


def process_senadores(legs: Tuple[str]):
    pass


def process_parlamentares(legs: Tuple[str]):
    deputados = process_deputados(legs)
    senadores = process_senadores(legs)

    # parlamentares <- deputados %>%
    #    bind_rows(senadores) %>%
    #    distinct() %>%
    #    arrange(legislatura)

    # return parlamentares


def update_parlamentares(parlamentares_filepath: str):
    legs = ("55", "56")
    csvfile = open(parlamentares_filepath, "r")
    # tmp = TemporaryFile()
    reader = csv.reader(csvfile, delimiter=",")

    headers = next(reader, None)
    current_parlamentares = filter(lambda row: row[0] in legs, reader)

    new_parlamentares = process_parlamentares(legs)
