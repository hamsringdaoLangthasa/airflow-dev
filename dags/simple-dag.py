from airflow import DAG
import pendulum

from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

def _check_accuracy():
    accuracy = 1
    if accuracy >= 1:
        return ["accurate", "top_accurate"]
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
    top_accurate = EmptyOperator(task_id="top_accurate")
    inaccurate = EmptyOperator(task_id="inaccurate")

    publish_ml = PythonOperator(
        task_id="publish_ml",
        python_callable=lambda: print("Publishing ML model..."),
        trigger_rule="none_failed_min_one_success"
    )

    end = EmptyOperator(task_id="end")

    start >> training_ml >> check_accuracy >> [ accurate, top_accurate, inaccurate ] >> publish_ml >> end