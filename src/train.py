import joblib
import mlflow.sklearn
import pandas as pd
from mlflow.models import infer_signature
from sklearn.linear_model import LogisticRegression

mlflow.set_tracking_uri("http://127.0.0.1:5000")


def train_model():
    X = pd.read_csv("intermediate/X_train_preprocessed.csv")
    y = pd.read_csv("intermediate/y_train.csv")

    # dummy training logic
    model = LogisticRegression()
    model.fit(X, y)

    y_pred = model.predict(X)

    joblib.dump(model, "artifacts/model.joblib")
    signature = infer_signature(X, y_pred)

    mlflow.sklearn.log_model(model, "model", signature=signature)
