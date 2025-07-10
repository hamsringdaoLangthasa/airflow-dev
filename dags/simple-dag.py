from airflow import DAG
import pendulum

from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

def _check_accuracy():
    accuracy = 0.85
    if accuracy > 0.8:
        return "accurate"
    else:
        return "inaccurate"

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

    check_accuracy = BranchPythonOperator(
        task_id="check_accuracy",
        python_callable=_check_accuracy,
    )

    accurate = EmptyOperator(task_id="accurate")
    inaccurate = EmptyOperator(task_id="inaccurate")

    end = EmptyOperator(task_id="end")

    start >> training_ml >> check_accuracy >> [ accurate, inaccurate ] >> end