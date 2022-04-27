import csv
import logging
import argparse
import tweepy
from dotenv import dotenv_values


import os

# to get the current working directory
directory = os.getcwd()

print("*" * 30)
print(directory)


class Parser:
    def __init__(self):
        parser = argparse.ArgumentParser()
        # Add an argument
        parser.add_argument("--users", type=str, required=True, help="user to searh")
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
        with open(self.args.get("search", default)) as search:
            return [line.rstrip() for line in search]

    def getUsers(self, client):
        felipeneto = "felipeneto"
        jairbolsonaro = "jairbolsonaro"
        marcelofreixo = "marcelofreixo"
        with open(self.args.get("users", [jairbolsonaro, marcelofreixo])) as users:
            return client.get_users(usernames=[line.rstrip() for line in users])


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
        try:

            for response in tweepy.Paginator(
                self.client.get_users_tweets,
                self.user.id,
                start_time=self.start_time,
                end_time=self.end_time,
            ):
                # (ISO 8601/RFC 3339).
                if response.data:
                    print("Page response")
                    print(response)
                    print("end response")

                    self.get_page(response.data, csv)
        except Exception as e:
            print(e)


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

    # API_KEY = config["API_KEY"]
    # API_SECRET = config["API_SECRET"]
    BEARER_TOKEN = config["BEARER_TOKEN"]

    # parser = Parser()
    client = tweepy.Client(BEARER_TOKEN)

    # parlamentares = Parlamentares(pargs=parser.get_args())
    # users = parlamentares.getUsers(client)

    # for user in users.data:

    #     print("\n\n\n")
    #     print("-" * 40)
    #     csv = TweetsCSV(user.username)
    #     csv.open_file()
    #     print(user.username)
    #     parlamentar = Tweets(user, client, parser.get_args(), parlamentares)
    #     parlamentar.get_users_tweets(csv)

    response = client.search_recent_tweets("Tweepy")
    # The method returns a Response object, a named tuple with data, includes,
    # errors, and meta fields
    print(response.meta)

    # In this case, the data field of the Response returned is a list of Tweet
    # objects
    tweets = response.data

    # Each Tweet object has default ID and text fields
    for tweet in tweets:
        print(tweet.id)
        print(tweet.text)
        print(type(tweet))

    # By default, this endpoint/method returns 10 results
    # You can retrieve up to 100 Tweets by specifying max_results
    response = client.search_recent_tweets("Tweepy", max_results=100)

    return 1


if __name__ == "__main__":
    main()
