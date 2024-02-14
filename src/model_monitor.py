import pandas as pd
from evidently.metric_preset import DataDriftPreset
from evidently.report import Report


def take_action():
    pass


def model_monitor():
    report = Report(
        metrics=[
            DataDriftPreset(),
        ]
    )

    df_ref = pd.read_csv("dataset/train.csv")
    df_live = pd.read_csv("inference/input/input_13-02-2024.csv")

    report.run(reference_data=df_ref, current_data=df_live)

    report = report.as_dict()

    if report["metrics"][0]["result"]["number_of_drifted_columns"] > 0:
        print("Data drift detected!")
        take_action()

    report.save_json("report.json")
    report.save_html("report.html")


if __name__ == "__main__":
    model_monitor()
