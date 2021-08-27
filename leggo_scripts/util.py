from typing import List

from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

from leggo_scripts import update_leggo_data


def task_builder(task_name: str, Operator=BashOperator, trigger_rule="all_done"):
    task_command = getattr(update_leggo_data, task_name, None)

    if task_command is None:
        raise Exception(f"Task {task_name} could not be found")

    task = Operator(
        task_id=f"task_{task_name}",
        bash_command=task_command(),
        trigger_rule=trigger_rule,
    )

    return task


def linear_task_queue(tasks_names: List[str]):
    dummy_task = DummyOperator(
        task_id="dummy_task",
    )

    prev_task = dummy_task
    tasks = []

    for task_name in tasks_names[::-1]:
        task = task_builder(task_name)
        tasks.append(task)

        prev_task << task  # Queue current_task
        prev_task = task

    return tasks
