from requests import post
from os import getenv
import json
import traceback


def send_tweets(**kwargs) -> None:
    task_instance = kwargs['task_instance']
    tweets = task_instance.xcom_pull(key='tweets')
    BACKEND_HOST = getenv("BACKEND_HOST")
    print('\n'*10)
    print('-'*50)
    print('send tweets task')
    print(type(tweets))
    for tweet in tweets:
        print(tweet)
    headers = {
        "Content-type": "application/json",
    }
    data = {
        'tweets': tweets,

    }
    try:
        response = post(f"{BACKEND_HOST}/tweets/",
                        headers=headers, data=json.dumps(tweets))
        print(response.content)
        print(response)
        # print(json.dumps(response.content))
    except Exception as e:
        print(traceback.format_exc())
        print('-' * 30)
        print(e)
        # raise Exception('Req falhou')


if __name__ == "__main__":
    send_tweets()
