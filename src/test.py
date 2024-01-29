import joblib
import mlflow
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
)

from .preprocess import preprocess


def test_model():
    model = joblib.load("artifacts/model.joblib")
    df_test = pd.read_csv("dataset/test.csv")
    y_true = df_test["y"].replace({"yes": 1, "no": 0}).values

    df_test = preprocess(df_test)

    y_pred = model.predict(df_test)

    accuracy = accuracy_score(y_true=y_true, y_pred=y_pred)
    precision = precision_score(y_true=y_true, y_pred=y_pred)
    recall = recall_score(y_true=y_true, y_pred=y_pred)

    mlflow.log_metric("accuracy", accuracy)
    mlflow.log_metric("precision", precision)
    mlflow.log_metric("recall", recall)

    print(confusion_matrix(y_true=y_true, y_pred=y_pred))


if __name__ == "__main__":
    test_model()
