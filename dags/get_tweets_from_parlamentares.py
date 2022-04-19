import csv
import logging
import tweepy
import argparse
from dotenv import dotenv_values
import os


class Parser:
    def __init__(self):
        parser = argparse.ArgumentParser()
        # Add an argument
        parser.add_argument("--user", type=str, required=True, help="user to searh")
        parser.add_argument(
            "--start", type=str, required=False, help="start date of tweets"
        )
        parser.add_argument(
            "--end", type=str, required=False, help="end date of tweets"
        )
        parser.add_argument(
            "--search", type=str, required=False, help="the text you want to search"
        )

        # Parse the argument
        args = parser.parse_args()

        self.args = args

    def get_args(self):
        return vars(self.args)


class TweetsCSV:

    """Escreve os tweets de parlamentares em arquivo"""

    def __init__(self, name, folder="./tweets"):
        self.name = name
        self.folder = folder
        self.full_path = f"{folder}/{name}.csv"

    def open_file(self):
        with open(self.full_path, "w", newline="") as file:
            writer = csv.writer(file)
            header = ["id", "text"]
            writer.writerow(header)

    def write_tweets(self, id, text):

        with open(self.full_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([id, text])


class Parlamentares:
    def __init__(self, pargs=None):
        self.args = pargs

    def getSearchTags(self):
        relator = "orlando"
        registro = "2630/2020"
        default = ["fake news", "fake", "news", relator, registro]
        return [self.args.get("search")] if self.args.get("search") else default

    def getUsers(self, client):
        felipeneto = "felipeneto"
        jairbolsonaro = "jairbolsonaro"
        marcelofreixo = "marcelofreixo"

        return client.get_users(
            usernames=self.args.get("user", [jairbolsonaro, marcelofreixo])
        )


class Tweets:
    def __init__(self, user, client, pargs, tags):
        self.user = user
        self.client = client
        self.start_time = pargs.get("start", "2021-10-13T15:42:15.000Z")
        self.end_time = pargs.get("end", "2022-04-13T13:00:15.000Z")
        self.tags = tags

    @staticmethod
    def filterByList(text, list):
        tags = set(list)
        found = []
        for item in tags:
            if item.lower() in text.lower():
                found.append(item)

        return sorted(found) if len(found) else None

    def get_page(self, page, csv):

        for item in page:
            did_found = self.filterByList(item.text, self.tags.getSearchTags())

            if did_found:
                print("Did found:")
                print(did_found)
                print(item.id)
                print(item.text)
                csv.write_tweets(item.id, item.text)

    def get_users_tweets(self, csv):

        for response in tweepy.Paginator(
            self.client.get_users_tweets,
            self.user.id,
            start_time=self.start_time,
            end_time=self.end_time,
        ):
            # (ISO 8601/RFC 3339).
            if response.data:
                self.get_page(response.data, csv)
            else:
                err = "Close account. Needs perm"
                # logger.error(err)
                print(err)


class Logger:
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(
        filename="./log",
        level=logging.DEBUG,
        format=LOG_FORMAT,
        filemode="w",
    )

    logger = logging.getLogger()
    print("Start")


def main() -> None:
    config = dotenv_values(f".env")

    BEARER_TOKEN = config["BEARER_TOKEN"]

    parser = Parser()
    client = tweepy.Client(BEARER_TOKEN)

    parlamentares = Parlamentares(pargs=parser.get_args())
    users = parlamentares.getUsers(client)

    for user in users.data:

        print("\n\n\n")
        print("-" * 40)
        csv = TweetsCSV(user.username)
        csv.open_file()
        print(user.username)
        parlamentar = Tweets(user, client, parser.get_args(), parlamentares)
        parlamentar.get_users_tweets(csv)


if __name__ == "__main__":
    main()
