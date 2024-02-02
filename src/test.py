import mlflow
import pandas as pd
from mlflow.sklearn import load_model
from prefect import task
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
)


@task
def test_model_performance():
    model = load_model("model_dir")
    X_test_preprocessed = pd.read_csv("intermediate/X_test_preprocessed.csv")
    y_true = pd.read_csv("intermediate/y_test.csv").values

    y_pred = model.predict(X_test_preprocessed)

    accuracy = accuracy_score(y_true=y_true, y_pred=y_pred)
    precision = precision_score(y_true=y_true, y_pred=y_pred)
    recall = recall_score(y_true=y_true, y_pred=y_pred)

    mlflow.log_metric("test_accuracy", accuracy)
    mlflow.log_metric("test_precision", precision)
    mlflow.log_metric("test_recall", recall)

    print(confusion_matrix(y_true=y_true, y_pred=y_pred))


if __name__ == "__main__":
    test_model_performance()
