from sklearn.linear_model import LogisticRegression
import pandas as pd
import joblib


def train():
    X = pd.read_csv("intermediate/X_train_preprocessed.csv")
    y = pd.read_csv("intermediate/y_train.csv")

    # dummy training logic
    model = LogisticRegression()
    model.fit(X, y)

    joblib.dump(model, "artifacts/model.joblib")

