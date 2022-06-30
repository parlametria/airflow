from sys import argv

from src.process_parlamentares import update_parlamentares


def main():
    EXPORT_CSV_FOLDERPATH = argv[1:][0]
    CSV_FILENAME = argv[1:][1]

    update_parlamentares("".join([EXPORT_CSV_FOLDERPATH, CSV_FILENAME]))

    return 0


if __name__ == "__main__":
    main()
