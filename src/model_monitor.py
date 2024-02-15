from time import gmtime, strftime

import pandas as pd
from evidently.metric_preset import DataDriftPreset
from evidently.report import Report
from prefect import flow


def take_action():
    pass


@flow(log_prints=True)
def model_monitor():
    report = Report(
        metrics=[
            DataDriftPreset(),
        ]
    )

    curr = strftime("%d-%m-%Y", gmtime())
    dataset_path = f"inference/input/input_{curr}.csv"

    df_ref = pd.read_csv("dataset/train.csv")
    df_live = pd.read_csv(dataset_path)

    report.run(reference_data=df_ref, current_data=df_live)

    report = report.as_dict()

    if report["metrics"][0]["result"]["number_of_drifted_columns"] > 0:
        print("Data drift detected!")
        take_action()



if __name__ == "__main__":
    model_monitor()
