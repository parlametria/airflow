import tweepy
# from dotenv import dotenv_values
from os import getenv
from datetime import datetime, timedelta


class Requisicao:
    def __init__(self):
        self.tweet = {
            "id_tweet": "",
            "id_author": "",
            "text": "",
            "data_criado": "",
            "likes": "",
            "retweets": "",
            "respostas": "",
        }

        self.tweets = []

    def get_paginate(self, req):
        counter = 0

        print(req)

        for page in req:
            for tweet in page.data:
                counter = counter + 1
                new_tweet = {
                    "id_tweet": tweet.id,
                    "id_author": tweet.author_id,
                    "text": tweet.text,
                    "data_criado": datetime.strftime(tweet.created_at, '%Y-%m-%d'),
                    "likes": tweet.public_metrics.get('like_count'),
                    "retweets": tweet.public_metrics.get('retweet_count'),
                    "respostas": tweet.public_metrics.get('reply_count')
                }
                self.tweets.append(new_tweet)

    def get_recent(self, search, id, end_time, start_time, order='relevancy', n_results=10, **kwargs):
        BEARER_TOKEN = getenv("BEARER_TOKEN")
        client = tweepy.Client(BEARER_TOKEN)

        expansions = ['author_id']
        # https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
        fields = ['created_at', 'public_metrics']

        req = tweepy.Paginator(client.search_recent_tweets,
                               search,
                               end_time=end_time,
                               start_time=start_time,
                               max_results=n_results,
                               sort_order=order,
                               expansions=expansions,
                               tweet_fields=fields)

        self.get_paginate(req)
        return req


def main(**kwargs) -> None:
    req = Requisicao()
    response = req.get_recent(**kwargs['dag_run'].conf)
    task_instance = kwargs['task_instance']
    print(req.tweets)
    task_instance.xcom_push(key='tweets', value=req.tweets)


if __name__ == "__main__":
    main()
