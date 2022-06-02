from typing import List
from airflow.operators.python_operator import PythonOperator
from tasks.process_new_tweets.get_tweets import main
from tasks.process_new_tweets.send_tweets import send_tweets


def process_new_tweets_tasks() -> List[PythonOperator]:

    # t1 = PythonOperator(
    #     task_id="python_caller",
    #     python_callable=main,
    #     op_kwargs={'has_command': False},
    # )

    get_tweets = PythonOperator(
        task_id="get_tweets",
        python_callable=main,
    )

    _send_tweets = PythonOperator(
        task_id='send_tweets',
        python_callable=send_tweets,
    )

    return [get_tweets, _send_tweets]
