from enum import Enum

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder, StandardScaler
import pandas as pd


class DatasetType(Enum):
    TRAIN = 1
    TEST = 2
    VAL = 3


def preprocess(df, dataset_type=DatasetType.TRAIN):
    df.marital = df.marital.replace("married", 1)
    df.marital = df.marital.replace("single", 0)
    df.marital = df.marital.replace("divorced", 2)
    df.default = df.default.replace(["no", "yes"], [0, 1])
    df.housing = df.housing.replace(["no", "yes"], [0, 1])
    df.loan = df.loan.replace(["no", "yes"], [0, 1])

    x = df.drop("y", axis=1)
    # y = df["y"]

    # if it's a training dataset, make a pipeline and save it
    # otherwise, use the saved pipeline for transform
    if dataset_type == DatasetType.TRAIN:
        numerical_features = []
        categorical_features = []
        for col in list(x.columns):
            if df[col].dtype == "int64" and col != "marital":
                numerical_features.append(col)
            else:
                categorical_features.append(col)

        nums_pipeline = Pipeline(
                        [
                            ("StandardScaler", StandardScaler()),
                            ("MinMaxScaler", MinMaxScaler())
                        ]
                    )

        cats_pipeline = Pipeline([("CategoricalEncoder", OrdinalEncoder())])

        full_pipeline = ColumnTransformer(
            [
                ("nums", nums_pipeline, numerical_features),
                ("cats", cats_pipeline, categorical_features),
            ]
        )
        df_preprocessed = pd.DataFrame(full_pipeline.fit_transform(x))
        joblib.dump(full_pipeline, "artifacts/preprocessing_pipeline.joblib")
    else:
        pass

    return df_preprocessed


if __name__ == "__main__":
    pd.set_option('future.no_silent_downcasting', True)
    train_df = pd.read_csv("dataset/train.csv")
    train_df_preprocessed = preprocess(train_df)
    print(train_df_preprocessed.head(10))
