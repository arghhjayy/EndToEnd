import warnings

import mlflow
import pandas as pd
from prefect import flow

from src.preprocess import preprocess
from src.test import test_model
from src.train import train_model

warnings.filterwarnings("ignore")


@flow(log_prints=True)
def main():
    with mlflow.start_run():
        print("MLFlow run started")
        # preprocess train data
        train_df = pd.read_csv("dataset/train.csv")
        X_train, y_train = train_df.loc[:"y"], train_df["y"]
        y_train = y_train.replace({"no": 0, "yes": 1})
        X_train_preprocessed = preprocess(X_train)
        X_train_preprocessed.to_csv(
            "intermediate/X_train_preprocessed.csv", index=False
        )
        y_train.to_csv("intermediate/y_train.csv", index=False)

        # preprocess test data
        test_df = pd.read_csv("dataset/test.csv")
        X_test, y_test = test_df.loc[:"y"], test_df["y"]
        y_test = y_test.replace({"no": 0, "yes": 1})
        X_test_preprocessed = preprocess(X_test)
        X_test_preprocessed.to_csv(
            "intermediate/X_test_preprocessed.csv", index=False
        )
        y_test.to_csv("intermediate/y_test.csv", index=False)

        train_model()
        test_model()


if __name__ == "__main__":
    main()
