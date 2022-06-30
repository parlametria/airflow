from dataclasses import dataclass
from typing import Dict, Union

# from tasks.atualiza_parlamentares.constants import CAMARA, SENADO
from .constants import CAMARA, SENADO


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
    em_exercicio: Union[int, str]

    def to_linedata(self):
        return [
            self.legislatura,
            self.id_parlamentar,
            self.id_parlamentar_parlametria,
            self.casa,
            self.nome_eleitoral,
            self.nome_civil,
            self.cpf,
            self.sexo,
            self.partido,
            self.uf,
            self.situacao,
            self.em_exercicio,
        ]


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
    mandato = (
        json["Mandatos"]["Mandato"][0]
        if type(json["Mandatos"]["Mandato"]) == list
        else json["Mandatos"]["Mandato"]
    )

    primeira_legis = mandato["PrimeiraLegislaturaDoMandato"]["NumeroLegislatura"]
    segunda_legs = mandato["SegundaLegislaturaDoMandato"]["NumeroLegislatura"]

    em_exercicio = 1 if json["legislatura"] in (primeira_legis, segunda_legs) else 0

    return Parlamentar(
        legislatura=json["legislatura"],
        id_parlamentar=id_parlamentar,
        id_parlamentar_parlametria="2" + id_parlamentar,
        casa=SENADO,
        nome_eleitoral=dict.get(
            json["IdentificacaoParlamentar"], "NomeParlamentar", "NA"
        ),
        nome_civil=dict.get(
            json["IdentificacaoParlamentar"], "NomeCompletoParlamentar", "NA"
        ),
        cpf="NA",
        sexo=dict.get(json["IdentificacaoParlamentar"], "SexoParlamentar")[0] or "NA",
        partido=dict.get(
            json["IdentificacaoParlamentar"], "SiglaPartidoParlamentar", "NA"
        ),
        uf=dict.get(mandato, "UfParlamentar", "NA"),
        situacao=dict.get(mandato, "DescricaoParticipacao", "NA"),
        em_exercicio=em_exercicio,
    )
