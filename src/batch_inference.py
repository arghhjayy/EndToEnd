import os
import tomllib
from time import gmtime, strftime

import pandas as pd
from mlflow.sklearn import load_model
from prefect import flow

from data_classes import DatasetType
from preprocess import load_and_preprocess


@flow(log_prints=True)
def infer():
    os.environ["TESTING"] = "TRUE"
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    model = load_model("model_dir")
    df = load_and_preprocess(DatasetType.BATCH_INFER, config=config)

    y_infer = model.predict(df)

    y_infer = pd.DataFrame(y_infer, columns=["pred"])

    curr = strftime("%d-%m-%Y", gmtime())
    dataset_path = config["inference"]["output_dir"] + f"/output_{curr}.csv"

    y_infer.to_csv(dataset_path, index=False)


if __name__ == "__main__":
    # dev:
    os.environ["TESTING"] = "TRUE"
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    infer(config)
