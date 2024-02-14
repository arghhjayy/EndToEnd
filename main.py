import tomllib
import warnings

import mlflow
from prefect import flow

from src.enum_classes import DatasetType
from src.preprocess import load_and_preprocess
from src.test import test_model_performance
from src.train import train_model

warnings.filterwarnings("ignore")


@flow(log_prints=True)
def main():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("binary-classification")

    with mlflow.start_run() as run:
        config["run_id"] = run.info.run_id
        current_experiment = dict(
            mlflow.get_experiment_by_name("binary-classification")
        )
        config["experiment_id"] = current_experiment["experiment_id"]
        print("MLFlow run started")
        # preprocess train data
        load_and_preprocess(dataset=DatasetType.TRAIN, config=config)
        # preprocess test data
        load_and_preprocess(dataset=DatasetType.TEST, config=config)

        train_model()
        test_model_performance()


if __name__ == "__main__":
    main()
