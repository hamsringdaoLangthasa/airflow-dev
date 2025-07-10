from airflow import DAG
import pendulum

from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

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

    training_ml = PythonOperator(
        task_id="training_ml",
        python_callable=lambda: print("Training ML model..."),
    )

    end = EmptyOperator(task_id="end")

    start >> training_ml >> end