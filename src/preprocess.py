import os
from time import gmtime, strftime

import joblib
import mlflow
import pandas as pd
from prefect import task
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder, StandardScaler

from src.data_classes import DatasetType


@task
def preprocess(df, config=None, dataset_type=DatasetType.TRAIN):
    df.marital = df.marital.replace({"married": 1})
    df.marital = df.marital.replace({"single": 0})
    df.marital = df.marital.replace({"divorced": 2})
    df.default = df.default.replace({"no": 0, "yes": 1})
    df.housing = df.housing.replace({"no": 0, "yes": 1})
    df.loan = df.loan.replace({"no": 0, "yes": 1})

    X = df.drop("y", axis=1)

    pipeline_name = "preprocessing_pipeline.joblib"
    pipeline_path_local = f"artifacts/{pipeline_name}"

    # if it's a training dataset, make a pipeline and save it
    # otherwise, use the saved pipeline for transform
    if dataset_type == DatasetType.TRAIN:
        numerical_features = []
        categorical_features = []
        for col in list(X.columns):
            if df[col].dtype == "int64" and col != "marital":
                numerical_features.append(col)
            else:
                categorical_features.append(col)

        nums_pipeline = Pipeline(
            [
                ("StandardScaler", StandardScaler()),
                ("MinMaxScaler", MinMaxScaler()),
            ]
        )

        cats_pipeline = Pipeline([("CategoricalEncoder", OrdinalEncoder())])

        full_pipeline = ColumnTransformer(
            [
                ("nums", nums_pipeline, numerical_features),
                ("cats", cats_pipeline, categorical_features),
            ]
        )
        full_pipeline.fit(X)
        df_preprocessed = pd.DataFrame(
            full_pipeline.transform(X), columns=X.columns
        )

        joblib.dump(full_pipeline, pipeline_path_local)

        if not os.environ.get("TESTING"):
            mlflow.log_artifact(
                pipeline_path_local,
                run_id=config["run_id"],
            )
    else:
        # BUG: load pipeline and transform when a train run is already done
        pipeline_path_mlflow = os.path.join(
            "mlartifacts",
            config["experiment_id"],
            config["run_id"],
            "artifacts",
            pipeline_name,
        )

        full_pipeline = joblib.load(pipeline_path_mlflow)

        df_preprocessed = pd.DataFrame(
            full_pipeline.transform(X), columns=X.columns
        )

    return df_preprocessed


def load_and_preprocess(dataset: DatasetType = 1, config=None) -> pd.DataFrame:
    match dataset:  # noqa
        case DatasetType.TRAIN:
            print("Using train data")
            dataset_path = config["data"]["train_path"]
        case DatasetType.TEST:
            print("Using test data")
            dataset_path = config["data"]["test_path"]
        case 3:
            curr = strftime("%d-%m-%Y", gmtime())
            print("done")
            dataset_path = (
                config["inference"]["input_dir"] + f"/input_{curr}.csv"
            )
        case _:
            raise ValueError(
                f"""Please pass a valid value to param 'dataset',
                allowed values: {[t.value for t in DatasetType]}"""
            )

    df = pd.read_csv(dataset_path)
    X, y = df.loc[:"y"], df["y"]
    y = y.replace({"no": 0, "yes": 1})
    if os.environ.get("TESTING", False):
        X_preprocessed = preprocess.fn(X)
    else:
        X_preprocessed = preprocess(X, config=config, dataset_type=dataset)
    intermediate_dir = config["data"]["intermediate_data_dir"]
    X_preprocessed.to_csv(
        f"{intermediate_dir}/X_{dataset}_preprocessed.csv", index=False
    )
    y.to_csv(f"{intermediate_dir}/y_{dataset}.csv", index=False)

    if os.environ.get("TESTING", False):
        return X_preprocessed
