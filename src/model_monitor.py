import smtplib
import tomllib
from email.message import EmailMessage
from time import gmtime, strftime

import pandas as pd
from evidently.metric_preset import DataDriftPreset
from evidently.report import Report
from prefect import flow


def send_email(sender_email, sender_password, recipient_email, subject, body):
    # Create the EmailMessage object
    message = EmailMessage()
    message.set_content(body)
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = recipient_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Use TLS encryption
        server.login(sender_email, sender_password)

        server.send_message(message)


def take_action(config):
    send_email(
        sender_email=config["sender_email"],
        sender_password=config["sender_password"],
        recipient_email=config["to_email"],
        subject="Data drift detected in the model!",
        body="""Hello,
                Data drift has been detected on the deployed model.
                Please check""",
    )


@flow(log_prints=True)
def model_monitor(config=None):
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
        take_action(config=config["alert"])


if __name__ == "__main__":
    with open("config.toml", "rb") as f:
        config = tomllib.load(f)
    model_monitor(config)
