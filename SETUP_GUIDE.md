# RetailPulse - Setup Guide

## 1. Requirements
- Windows with WSL2 and Ubuntu
- Python
- Apache Airflow 3.3.2
- Jupyter Notebook

## 2. Open Ubuntu
Run this command in PowerShell:

```powershell
wsl -d Ubuntu
```

## 3. Activate the Airflow environment
Run these commands in Ubuntu:

```bash
source ~/airflow_venv/bin/activate
python --version
airflow version
```

## 4. Start Airflow
Run in Ubuntu:

```bash
airflow standalone
```

Keep this terminal running while using Airflow. Open the Airflow UI at:

http://localhost:8080

## 5. Pipeline
DAG file: `dags/retailpulse_pipeline.py`

Retraining script: `retrain_churn.py`

The DAG runs the churn model retraining task on a daily schedule when Airflow is running.

## 6. Important note
The original `terminal_commands.txt` contains raw command history. Review it for private details before sharing it. Never share passwords, tokens, or Airflow credentials.
