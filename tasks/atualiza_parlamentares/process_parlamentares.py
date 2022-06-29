import csv

from typing import Tuple, Generator, List
from tempfile import TemporaryFile

from tasks.atualiza_parlamentares.fetch_deputados import fetch_deputados
from tasks.atualiza_parlamentares.fetch_senadores import fetch_senadores
from tasks.atualiza_parlamentares.schemas import (
    deputado_json_to_parlamentar,
    senador_json_to_parlamentar,
    Parlamentar,
)

ParlaGen = Generator[Parlamentar, None, None]


def process_deputados(legs: Tuple[str]) -> ParlaGen:
    for data in fetch_deputados(legs):
        yield deputado_json_to_parlamentar(data)


def process_senadores(legs: Tuple[str]) -> ParlaGen:
    for data in fetch_senadores(legs):
        yield senador_json_to_parlamentar(data)


def join_parlamentares_by_leg(
    legs: Tuple[str], deputados: ParlaGen, senadores: ParlaGen
) -> List[Parlamentar]:
    """
    Keep deputados and senadores ordered by legislatura, ex:
        55, deputado\n
        55, senador\n
        56, deputado\n
        56, senador\n
    """

    ordered = dict()
    for leg in legs:
        ordered[leg] = []

    for dep in deputados:
        ordered[dep.legislatura].append(dep)

    for sen in senadores:
        ordered[sen.legislatura].append(sen)

    joined = []
    for leg in legs:
        for parla in ordered[leg]:
            joined.append(parla)

    return joined


def process_parlamentares(legs: Tuple[str]) -> List[Parlamentar]:
    deputados = process_deputados(legs)
    senadores = process_senadores(legs)

    return join_parlamentares_by_leg(legs, deputados, senadores)


def update_parlamentares(parlamentares_filepath: str):
    legs = ("55", "56")

    csvfile_read = open(parlamentares_filepath, "r")
    tmpcsv = TemporaryFile(mode="r+")

    reader = csv.reader(csvfile_read, delimiter=",")
    writer = csv.writer(tmpcsv, delimiter=",")

    headers = next(reader)
    parlamentares_other_legs = filter(lambda row: row[0] not in legs, reader)

    # Write on TemporaryFile the filtered parlamentares from old legislatura
    # and add new data from the fetched legs
    writer.writerow(headers)
    writer.writerows(parlamentares_other_legs)

    for parlamentar in process_parlamentares(legs):
        writer.writerow(parlamentar.to_linedata())

    csvfile_read.close()

    # go to begin of tmp file to copy all data to parlamentares_filepath
    tmpcsv.seek(0)

    # Override data of parlamentares_filepath with data from tmp file
    csvfile_override = open(parlamentares_filepath, "w")
    writer = csv.writer(csvfile_override, delimiter=",")
    reader = csv.reader(tmpcsv, delimiter=",")
    writer.writerows(reader)

    csvfile_override.close()
    tmpcsv.close()  # delete temporary file
