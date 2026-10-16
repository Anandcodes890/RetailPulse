import os
import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score

DATA_PATH = "/mnt/c/Users/aanan/Desktop/RetailPulse/online_retail_II.xlsx"
MODEL_PATH = "/mnt/c/Users/aanan/Desktop/RetailPulse/retailpulse_churn_model.pkl"


def train_churn_model():
    print("Loading RetailPulse dataset...")
    df = pd.read_excel(DATA_PATH)

    df.columns = df.columns.str.strip()

    required = [
        "Invoice", "Quantity", "InvoiceDate",
        "Price", "Customer ID"
    ]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
    df["Customer ID"] = pd.to_numeric(df["Customer ID"], errors="coerce")

    df = df.dropna(subset=["Invoice", "InvoiceDate", "Customer ID"])
    df = df[(df["Quantity"] > 0) & (df["Price"] > 0)]
    df = df[~df["Invoice"].astype(str).str.startswith("C")]

    df["TotalSales"] = df["Quantity"] * df["Price"]

    snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    rfm = df.groupby("Customer ID").agg(
        Recency=("InvoiceDate", lambda x: (snapshot_date - x.max()).days),
        Frequency=("Invoice", "nunique"),
        Monetary=("TotalSales", "sum")
    ).reset_index()

    rfm["Churn"] = (rfm["Recency"] >= 90).astype(int)

    # Do not use Recency as a feature: it directly defines the target.
    feature_cols = ["Frequency", "Monetary"]
    X = rfm[feature_cols]
    y = rfm["Churn"]

    if y.nunique() < 2:
        raise ValueError("Training data contains only one churn class.")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric="logloss"
    )

    print("Training churn model...")
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1]

    print("Accuracy:", round(accuracy_score(y_test, predictions), 4))
    print("ROC-AUC:", round(roc_auc_score(y_test, probabilities), 4))

    joblib.dump(
        {"model": model, "features": feature_cols},
        MODEL_PATH
    )

    print("Retrained model saved to:", MODEL_PATH)


if __name__ == "__main__":
    train_churn_model()
