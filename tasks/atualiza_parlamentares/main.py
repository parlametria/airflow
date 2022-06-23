import csv
from tempfile import TemporaryFile

from tasks.atualiza_parlamentares.process_parlamentares import process_deputados

def main():
  legs = ("55", "56")
  process_deputados(legs)




if __name__ == "__main__":
  main()
