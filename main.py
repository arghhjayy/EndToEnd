import warnings

import mlflow
from prefect import flow

from src.preprocess import load_and_preprocess
from src.test import test_model_performance
from src.train import train_model

warnings.filterwarnings("ignore")


@flow(log_prints=True)
def main():
    with mlflow.start_run():
        print("MLFlow run started")
        # preprocess train data
        load_and_preprocess(dataset="train")
        # preprocess test data
        load_and_preprocess(dataset="test")

        train_model()
        test_model_performance()


if __name__ == "__main__":
    main()
