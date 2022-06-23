import requests
import json

from typing import List, Iterable, Tuple

from tasks.atualiza_parlamentares.constants import CAMARA_API_LINK, DEPUTADOS_PATH


def fetch_deputado(id: int):
    url = "".join([CAMARA_API_LINK, DEPUTADOS_PATH, "/", str(id)])
    response = requests.get(url)
    return response.json()

def fetch_all_deputados(ids: Iterable[int]):
    #return map(lambda id: fetch_deputado(id)['dados'], ids)
    data = fetch_deputado(list(ids)[0])['dados']
    #print(json.dumps(data, indent=4, sort_keys=True))
    return [data]

def fetch_deputados_by_leg(id_leg: str):
    url = "".join([CAMARA_API_LINK, DEPUTADOS_PATH, "?idLegislatura=", id_leg])
    response = requests.get(url)
    return response.json()


def fetch_deputados(legs: Tuple[str]):
    ids = set()
    legs_data = map(fetch_deputados_by_leg, legs)

    for leg in legs_data:
        for row in leg["dados"]:
            ids.add(row["id"])

    return fetch_all_deputados(ids)
