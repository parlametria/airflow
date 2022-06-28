import requests
import json

# from functools import lru_cache
from typing import List, Tuple, Dict

from tasks.atualiza_parlamentares.constants import (
    SENADO_API_LINK,
    SENADORES_PATH,
    SENADOR_PATH,
)


def fetch_mandato_senador(id: int):
    # https://legis.senado.leg.br/dadosabertos/senador/5573/mandatos?v=5
    url = "".join([SENADO_API_LINK, "/", SENADOR_PATH, str(id), "/mandatos.json"])
    response = requests.get(url)
    return response.json()


def fetch_senador_base_data(id: int):
    """
    https://legis.senado.leg.br/dadosabertos/senador/5573.json
    """
    url = "".join([SENADO_API_LINK, "/", SENADOR_PATH, str(id), ".json"])
    response = requests.get(url)
    return response.json()


def fetch_senadores_by_leg(id_leg: str) -> List[Dict]:
    """
    https://legis.senado.leg.br/dadosabertos/senador/lista/legislatura/55/55.json
    """
    url = "".join([SENADO_API_LINK, "/", SENADORES_PATH, id_leg, "/", id_leg, ".json"])
    response = requests.get(url)
    return response.json()


def fetch_senadores(legs: Tuple[str]):
    for leg in legs[:1]:
        print(f"Buscando senadores da legislatura {leg}")
        data = fetch_senadores_by_leg(leg)

        for senador in data["ListaParlamentarLegislatura"]["Parlamentares"][
            "Parlamentar"
        ][:1]:
            # print(json.dumps(senador, indent=4, sort_keys=True))
            senador["legislatura"] = leg
            yield senador
