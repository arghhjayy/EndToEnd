import os
from enum import Enum

import joblib
import mlflow
import pandas as pd
from prefect import task
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder, StandardScaler


class DatasetType(Enum):
    TRAIN = 1
    TEST = 2
    VAL = 3


@task
def preprocess(df, dataset_type=DatasetType.TRAIN):
    df.marital = df.marital.replace({"married": 1})
    df.marital = df.marital.replace({"single": 0})
    df.marital = df.marital.replace({"divorced": 2})
    df.default = df.default.replace({"no": 0, "yes": 1})
    df.housing = df.housing.replace({"no": 0, "yes": 1})
    df.loan = df.loan.replace({"no": 0, "yes": 1})

    X = df.drop("y", axis=1)

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

        joblib.dump(full_pipeline, "artifacts/preprocessing_pipeline.joblib")
        if not os.environ["TESTING"]:
            mlflow.log_artifact("artifacts/preprocessing_pipeline.joblib")
    else:
        pass

    return df_preprocessed


def load_and_preprocess(dataset: str = "train") -> pd.DataFrame:
    if dataset == "train":
        dataset_path = "dataset/train.csv"
    else:
        dataset_path = "dataset/test.csv"

    df = pd.read_csv(dataset_path)
    X, y = df.loc[:"y"], df["y"]
    y = y.replace({"no": 0, "yes": 1})
    if os.environ["TESTING"]:
        X_preprocessed = preprocess.fn(X)
    else:
        X_preprocessed = preprocess(X)
    X_preprocessed.to_csv(
        f"intermediate/X_{dataset}_preprocessed.csv", index=False
    )
    y.to_csv(f"intermediate/y_{dataset}.csv", index=False)

    if os.environ["TESTING"]:
        return X_preprocessed
