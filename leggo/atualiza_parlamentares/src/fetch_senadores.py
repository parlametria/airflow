import requests
import json

from typing import List, Tuple, Dict

from .constants import SENADO_API_LINK, SENADORES_PATH


def fetch_senadores_by_leg(id_leg: str) -> List[Dict]:
    """
    https://legis.senado.leg.br/dadosabertos/senador/lista/legislatura/55/55.json
    """
    url = "".join([SENADO_API_LINK, "/", SENADORES_PATH, id_leg, "/", id_leg, ".json"])
    response = requests.get(url)
    return response.json()


def fetch_senadores(legs: Tuple[str]):
    for leg in legs:
        print(f"Buscando senadores da legislatura {leg}")
        data = fetch_senadores_by_leg(leg)

        for senador in data["ListaParlamentarLegislatura"]["Parlamentares"][
            "Parlamentar"
        ]:
            # print(json.dumps(senador, indent=4, sort_keys=True))
            senador["legislatura"] = leg
            yield senador
