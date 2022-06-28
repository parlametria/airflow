import requests
import json

from typing import List, Iterable, Tuple, Dict

from tasks.atualiza_parlamentares.constants import CAMARA_API_LINK, DEPUTADOS_PATH


def fetch_deputado(id: int):
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

        for row in data["dados"][:1]:
            data = fetch_deputado(row["id"])
            data["dados"]["legislatura"] = leg

            yield data["dados"]
