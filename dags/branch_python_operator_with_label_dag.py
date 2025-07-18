"""Example DAG demonstrating the usage of the BranchPythonOperator."""

from airflow.sdk import DAG, Label
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import BranchPythonOperator
import random


with DAG(
    dag_id='branch_python_operator_with_label'
) as dag:

    run_this_first = EmptyOperator(
        task_id='run_this_first',
    )

    options = ['branch_a', 'branch_b', 'branch_c', 'branch_d']

    branching = BranchPythonOperator(
        task_id='branching',
        python_callable=lambda: random.choice(options),
    )

    run_this_first >> branching

    join = EmptyOperator(
        task_id='join',
        trigger_rule="none_failed_min_one_success",
    )

    for option in options:

        t = EmptyOperator(
            task_id=option,
        )

        empty_follow = EmptyOperator(
            task_id='follow_' + option,
        )

        # Label is optional here, but it can help identify more complex branches
        branching >> Label(option) >> t >> empty_follow >> join