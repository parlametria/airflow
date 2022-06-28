from dataclasses import dataclass
from typing import Dict

from tasks.atualiza_parlamentares.constants import CAMARA, SENADO


@dataclass
class Parlamentar:
    legislatura: int
    id_parlamentar: str
    id_parlamentar_parlametria: int
    casa: str
    nome_eleitoral: str
    nome_civil: str
    cpf: str
    sexo: str
    partido: str
    uf: str
    situacao: str
    em_exercicio: int


def deputado_json_to_parlamentar(json: Dict):
    return Parlamentar(
        legislatura=json["legislatura"],
        id_parlamentar=str(json["id"]),
        id_parlamentar_parlametria="1" + str(json["id"]),
        casa=CAMARA,
        nome_eleitoral=json["ultimoStatus"]["nomeEleitoral"].title(),
        nome_civil=json["nomeCivil"].title(),
        cpf=json["cpf"],
        sexo=json["sexo"],
        partido=json["ultimoStatus"]["siglaPartido"],
        uf=json["ultimoStatus"]["siglaUf"],
        situacao=json["ultimoStatus"]["condicaoEleitoral"],
        em_exercicio=1 if json["ultimoStatus"]["situacao"] == "Exercício" else 0,
    )


def senador_json_to_parlamentar(json: Dict):
    id_parlamentar = str(json["IdentificacaoParlamentar"]["CodigoParlamentar"])
    primeira_legis = json["Mandatos"]["Mandato"]["PrimeiraLegislaturaDoMandato"][
        "NumeroLegislatura"
    ]
    segunda_legs = json["Mandatos"]["Mandato"]["SegundaLegislaturaDoMandato"][
        "NumeroLegislatura"
    ]
    em_exercicio = 1 if json["legislatura"] in (primeira_legis, segunda_legs) else 0

    return Parlamentar(
        legislatura=json["legislatura"],
        id_parlamentar=id_parlamentar,
        id_parlamentar_parlametria="2" + id_parlamentar,
        casa=SENADO,
        nome_eleitoral=json["IdentificacaoParlamentar"]["NomeParlamentar"],
        nome_civil=json["IdentificacaoParlamentar"]["NomeCompletoParlamentar"],
        cpf="NA",
        sexo=json["IdentificacaoParlamentar"]["SexoParlamentar"][0],
        partido=json["IdentificacaoParlamentar"]["SiglaPartidoParlamentar"],
        uf=json["Mandatos"]["Mandato"]["UfParlamentar"],
        situacao=json["Mandatos"]["Mandato"]["DescricaoParticipacao"],
        em_exercicio=em_exercicio,
    )
