import joblib
import mlflow.sklearn
import pandas as pd
from mlflow.models import infer_signature
from prefect import task
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import GridSearchCV

mlflow.set_tracking_uri("http://127.0.0.1:5000")


@task
def train_model():
    X = pd.read_csv("intermediate/X_train_preprocessed.csv")
    y = pd.read_csv("intermediate/y_train.csv")
    y = y.values.ravel()

    # dummy training logic
    params = {
        "penalty": ["l1", "l2"],
        "tol": [0.0001, 0.0005, 0.0025, 0.01, 0.05, 0.1],
    }

    model = LogisticRegression(solver="liblinear")

    grid = GridSearchCV(
        model,
        param_grid=params,
        n_jobs=-1,
        cv=5,
        scoring="accuracy",
        verbose=1,
    )
    grid.fit(X, y)

    best_model = grid.best_estimator_
    best_params = grid.best_params_

    for k, v in best_params.items():
        mlflow.log_param(k, v)

    y_pred = best_model.predict(X)

    metrics = {
        "train_accuracy": accuracy_score(y_true=y, y_pred=y_pred),
        "train_recall": recall_score(y_true=y, y_pred=y_pred),
        "train_precision": precision_score(y_true=y, y_pred=y_pred),
    }

    for k, v in metrics.items():
        mlflow.log_metric(k, v)

    joblib.dump(best_model, "artifacts/model.joblib")
    signature = infer_signature(X, y_pred)

    mlflow.sklearn.log_model(
        best_model,
        "model",
        signature=signature,
        registered_model_name="grid_search",
    )
