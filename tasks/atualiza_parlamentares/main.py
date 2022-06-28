import csv
from tempfile import TemporaryFile

from tasks.atualiza_parlamentares.process_parlamentares import update_parlamentares

def main():
  legs = ("55", "56")
  #process_deputados(legs)
  # deputados = [d for d in process_deputados(legs)]
  # print(deputados)
  # process_senadores(legs)



  update_parlamentares("")




if __name__ == "__main__":
  main()
