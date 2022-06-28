import csv
import requests
import json

from typing import Tuple
from itertools import chain

from tasks.atualiza_parlamentares.fetch_deputados import fetch_deputados
from tasks.atualiza_parlamentares.fetch_senadores import fetch_senadores
from tasks.atualiza_parlamentares.schemas import (
    json_to_deputado,
    json_to_senador,
    Parlamentar,
)


CAMARA = "camara"
SENADO = "senado"
DEPUTADOS_PATH = "/api/v2/deputados"
CAMARA_API_LINK = "https://dadosabertos.camara.leg.br"
SENADO_API_LINK = "https://legis.senado.leg.br"


def format_deputado_data(deputado):
    deputado["nome_civil"] = deputado["nome_civil"].title()
    return deputado


def process_deputados(legs: Tuple[str]):
    for data in fetch_deputados(legs):
        yield json_to_deputado(data)


def process_senadores(legs: Tuple[str]):
    for data in fetch_senadores(legs):
        yield json_to_senador(data)


def process_parlamentares(legs: Tuple[str]):
    deputados = process_deputados(legs)
    senadores = process_senadores(legs)

    # join deputados and senadores as a singled parlamentar iterator
    return chain(deputados, senadores)


def update_parlamentares(parlamentares_filepath: str):
    legs = ("55", "56")
    # csvfile = open(parlamentares_filepath, "r")
    # tmp = TemporaryFile()
    # reader = csv.reader(csvfile, delimiter=",")

    # headers = next(reader, None)
    # current_parlamentares = filter(lambda row: row[0] in legs, reader)

    new_parlamentares = process_parlamentares(legs)

    for p in new_parlamentares:
        print(p)
