from datetime import datetime
from airflow.sdk import dag, task
import subprocess
import sys


@dag(
    dag_id="retailpulse_pipeline",
    start_date=datetime(2026, 10, 1),
    schedule="@daily",
    catchup=False,
    tags=["RetailPulse", "ML"],
)
def retailpulse_pipeline():

    @task
    def retrain_churn_model():
        script = "/mnt/c/Users/aanan/Desktop/RetailPulse/retrain_churn.py"

        result = subprocess.run(
            [sys.executable, script],
            check=True,
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        if result.stderr:
            print(result.stderr)

    retrain_churn_model()


retailpulse_pipeline()
