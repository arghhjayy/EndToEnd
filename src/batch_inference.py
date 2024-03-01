import os
import tomllib
from time import gmtime, strftime

import pandas as pd
from mlflow.sklearn import load_model
from prefect import flow

from db.utils import get_db_connection
from enum_classes import DatasetType
from preprocess import load_and_preprocess


@flow(log_prints=True)
def infer():
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)

    print(config)

    model = load_model("model_dir")
    df = load_and_preprocess(dataset=DatasetType.BATCH_INFER, config=config)

    y_infer = model.predict(df)

    y_infer = pd.DataFrame(y_infer, columns=["pred"])

    if config["inference"]["type"] == "csv":
        curr = strftime("%d-%m-%Y", gmtime())
        dataset_path = config["inference"]["output_dir"] + f"/output_{curr}.csv"

        os.makedirs("inference/output", exist_ok=True)

        y_infer.to_csv(dataset_path, index=False)
    else:
        engine = get_db_connection("INFERENCE")
        y_infer.to_sql(name="OUTPUT", con=engine, if_exists="replace", index=False)


if __name__ == "__main__":
    # dev:
    os.environ["TESTING"] = "TRUE"
    infer.fn()
