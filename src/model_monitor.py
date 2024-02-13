import pandas as pd
from evidently.metric_preset import DataDriftPreset
from evidently.report import Report


def model_monitor():
    report = Report(
        metrics=[
            DataDriftPreset(),
        ]
    )

    df_ref = pd.read_csv("dataset/train.csv")
    df_live = pd.read_csv("inference/input/input_13-02-2024.csv")

    report.run(reference_data=df_ref, current_data=df_live)
    
    report.save_json("report.json")
    report.save_html("report.html")


if __name__ == "__main__":
    model_monitor()
