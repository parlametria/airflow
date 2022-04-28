from typing import List
from airflow.operators.python_operator import PythonOperator
from tasks.process_new_tweets.main import main

def process_new_tweets_tasks() -> List[PythonOperator]:

    t1 = PythonOperator(
        task_id="python_caller",
        python_callable=main,
        op_kwargs={'has_command': False},
    )

    return [t1]
