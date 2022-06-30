import requests
import json

from typing import List, Iterable, Tuple, Dict

from .constants import CAMARA_API_LINK, DEPUTADOS_PATH

def fetch_deputado(id: int):
    print(f"\tBuscando deputado com id {id}")
    url = "".join([CAMARA_API_LINK, DEPUTADOS_PATH, "/", str(id)])
    response = requests.get(url)
    return response.json()


def fetch_deputados_by_leg(id_leg: str) -> List[Dict]:
    url = "".join([CAMARA_API_LINK, DEPUTADOS_PATH, "?idLegislatura=", id_leg])
    response = requests.get(url)
    return response.json()


def fetch_deputados(legs: Tuple[str]):
    for leg in legs:
        print(f"Buscando deputados da legislatura {leg}")
        data = fetch_deputados_by_leg(leg)

        for row in data["dados"]:
            data = fetch_deputado(row["id"])
            data["dados"]["legislatura"] = leg

            yield data["dados"]
