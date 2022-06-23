from dataclasses import dataclass, asdict
from typing import Optional, List

"""
{
  "id": 215042,
  "uri": "https: //dadosabertos.camara.leg.br/api/v2/deputados/215042",
  "nomeCivil": "RICARDO CORREA DE BARROS",
  "ultimoStatus": {
    "id": 215042,
    "uri": "https://dadosabertos.camara.leg.br/api/v2/deputados/215042",
    "nome": "Ricardo da Karol",
    "siglaPartido": "PDT",
    "uriPartido": "https://dadosabertos.camara.leg.br/api/v2/partidos/36786",
    "siglaUf": "RJ",
    "idLegislatura": 56,
    "urlFoto": "https://www.camara.leg.br/internet/deputado/bandep/215042.jpg",
    "email": "dep.ricardodakarol@camara.leg.br",
    "data": "2021-01-01T17:31",
    "nomeEleitoral": "Ricardo da Karol",
    "gabinete": {
      "nome": "274",
      "predio": "3",
      "sala": "274",
      "andar": null,
      "telefone": "3215-5274",
      "email": "dep.ricardodakarol@camara.leg.br"
    },
    "situacao": "Exercício",
    "condicaoEleitoral": "Efetivado",
    "descricaoStatus": null
  },
  "cpf": "59611456700",
  "sexo": "M",
  "urlWebsite": null,
  "redeSocial": [],
  "dataNascimento": "1959-10-27",
  "dataFalecimento": null,
  "ufNascimento": "RJ",
  "municipioNascimento": "Magé",
  "escolaridade": "Ensino Médio"
}
"""


@dataclass
class Gabinete:
    nome: Optional[str]
    predio: Optional[str]
    sala: Optional[str]
    andar: Optional[str]
    telefone: Optional[str]
    email: Optional[str]


@dataclass
class DeputadoStatus:
    id: str
    uri: Optional[str]
    nome: Optional[str]
    sigla_partido: Optional[str]
    uri_partido: Optional[str]
    sigla_uf: Optional[str]
    id_legislatura: int
    url_foto: Optional[str]
    email: Optional[str]
    data: Optional[str]
    nome_eleitoral: Optional[str]
    gabinete: Gabinete
    situacao: Optional[str]
    condicao_eleitoral: Optional[str]
    descricao_status: Optional[str]


@dataclass
class Deputado:
    id: str
    uri: str
    nome_civil: str
    ultimo_status: DeputadoStatus
    cpf: str
    sexo: str
    url_website: Optional[str]
    rede_social: List[str]
    data_nascimento: str
    data_falecimento: Optional[str]
    uf_nascimento: str
    municipio_nascimento: str
    escolaridade: str
    em_exercicio: int
    id_parlamentar_parlametria: str
    casa: str = "camara"


def json_to_deputado(json):
    return Deputado(
        id=str(json["id"]),
        uri=json["uri"],
        nome_civil=json["nomeCivil"].title(),
        ultimo_status=DeputadoStatus(
            id=str(json["ultimoStatus"]["id"]),
            uri=json["ultimoStatus"]["uri"],
            nome=json["ultimoStatus"]["nome"].title(),
            sigla_partido=json["ultimoStatus"]["siglaPartido"],
            uri_partido=json["ultimoStatus"]["uriPartido"],
            sigla_uf=json["ultimoStatus"]["siglaUf"],
            id_legislatura=json["ultimoStatus"]["idLegislatura"],
            url_foto=json["ultimoStatus"]["urlFoto"],
            email=json["ultimoStatus"]["email"],
            data=json["ultimoStatus"]["data"],
            nome_eleitoral=json["ultimoStatus"]["nomeEleitoral"].title(),
            gabinete=Gabinete(
                nome=json["ultimoStatus"]["gabinete"]["nome"],
                predio=json["ultimoStatus"]["gabinete"]["predio"],
                sala=json["ultimoStatus"]["gabinete"]["sala"],
                andar=json["ultimoStatus"]["gabinete"]["andar"],
                telefone=json["ultimoStatus"]["gabinete"]["telefone"],
                email=json["ultimoStatus"]["gabinete"]["email"],
            ),
            situacao=json["ultimoStatus"]["situacao"],
            condicao_eleitoral=json["ultimoStatus"]["condicaoEleitoral"],
            descricao_status=json["ultimoStatus"]["descricaoStatus"],
        ),
        cpf=json["cpf"],
        sexo=json["sexo"],
        url_website=json["urlWebsite"],
        rede_social=json["redeSocial"],
        data_nascimento=json["dataNascimento"],
        data_falecimento=json["dataFalecimento"],
        uf_nascimento=json["ufNascimento"],
        municipio_nascimento=json["municipioNascimento"],
        escolaridade=json["escolaridade"],
        em_exercicio=1 if json["ultimoStatus"]["situacao"] == "Exercício" else 0,
        id_parlamentar_parlametria = "1" + str(json["id"])
    )
