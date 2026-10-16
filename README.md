# RetailPulse – AI-Powered Customer Analytics & Demand Forecasting Platform

## Project Overview
RetailPulse is a retail analytics and machine learning project designed to analyze customer behavior, forecast demand, predict customer churn, and support inventory planning.

## Technologies Used
- Python
- Pandas and NumPy
- Matplotlib
- Scikit-learn
- XGBoost
- Prophet
- PyTorch (LSTM)
- MLflow
- Evidently AI
- Optuna
- Apache Airflow
- Jupyter Notebook

## Project Work
1. Data cleaning and preprocessing
2. Exploratory Data Analysis (EDA)
3. Sales trend analysis and visualization
4. RFM analysis and customer segmentation
5. K-Means clustering
6. Demand forecasting using Prophet and LSTM
7. Customer churn prediction using XGBoost
8. Inventory optimization
9. Hyperparameter tuning using Optuna
10. Data drift checks using Evidently AI
11. Experiment tracking with MLflow
12. Automated model retraining using Apache Airflow

## Main Files
- `RetailPulse.ipynb` - Main analysis and model development notebook
- `retrain_churn.py` - Model retraining script
- `dags/retailpulse_pipeline.py` - Airflow DAG
- `retailpulse_churn_model.pkl` - Saved churn model
- `mlflow.db` and `mlruns/` - MLflow experiment tracking data
- `online_retail_II.xlsx` - Dataset

## Airflow Pipeline
The `retailpulse_pipeline` DAG automates churn model retraining on a daily schedule when Airflow is running.

## Current Churn Model Evaluation
The latest training run reported:
- Accuracy: 0.6952
- ROC-AUC: 0.7242

These are preliminary results based on a proxy churn label and should not be treated as production performance.

## Notes
This project is for learning and demonstration. Model performance and business recommendations require further validation before production use.
