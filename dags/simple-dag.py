from airflow import DAG
import pendulum

from airflow.operators.empty import EmptyOperator

with DAG(
    dag_id="simple_dag",
    start_date=pendulum.datetime(2025, 7, 10, tz="UTC"),
    schedule="@daily",
    catchup=False,
    default_args={"owner": "Airflow", "retries": 3},
    tags=["example"],
) as dag:
    # Define tasks
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    start >> end