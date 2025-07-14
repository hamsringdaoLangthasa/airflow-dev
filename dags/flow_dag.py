from airflow import DAG
from airflow.operators.empty import EmptyOperator
import pendulum

with DAG(
    dag_id='flow_dag',
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    schedule="@daily",
    catchup=False,
    default_args={"owner": "Astro", "retries": 3},
    tags=["example"],
) as dag:

    start = EmptyOperator(task_id='start')

    task_a = EmptyOperator(task_id='task_a')
    task_b = EmptyOperator(task_id='task_b')
    task_c = EmptyOperator(task_id='task_c')

    end = EmptyOperator(task_id='end')

    start >> [task_a, task_b] >> task_c >> end
    start >> [task_a, task_b] >> task_c >> end