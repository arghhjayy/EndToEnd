import os
import random
from time import gmtime, strftime

import pandas as pd
from prefect import flow

from db.utils import get_db_connection


# generate data for dummy inference
@flow(log_prints=True)
def generate_data(size=1000, based_on="train", strategy="randomized", type="csv"):
    if based_on == "train":
        df = pd.read_csv("dataset/train.csv")
    else:
        df = pd.read_csv("dataset/test.csv")

    if strategy == "randomized":
        age = [random.randint(df.age.min(), df.age.max()) for _ in range(size)]
        job = [random.choice(df.job.unique()) for _ in range(size)]
        marital = [random.choice(df.marital.unique()) for _ in range(size)]
        education = [random.choice(df.education.unique()) for _ in range(size)]
        default = [random.choice(df.default.unique()) for _ in range(size)]
        balance = [random.randint(-300, 4000) for _ in range(size)]
        housing = [random.choice(df.housing.unique()) for _ in range(size)]
        loan = [random.choice(df.loan.unique()) for _ in range(size)]
        contact = [random.choice(df.contact.unique()) for _ in range(size)]
        day = [random.randint(1, 31) for _ in range(size)]
        month = [random.choice(df.month.unique()) for _ in range(size)]
        duration = [
            random.randint(df.duration.min(), df.duration.max()) for _ in range(size)
        ]
        campaign = [random.choice(df.campaign.unique()) for _ in range(size)]
        pdays = [random.choice([random.randint(0, 365), -1]) for _ in range(size)]
        previous = [random.choice(df.previous.unique()) for _ in range(size)]
        poutcome = [random.choice(df.poutcome.unique()) for _ in range(size)]
        y = [random.choice(df.y.unique()) for _ in range(size)]

        data = [
            age,
            job,
            marital,
            education,
            default,
            balance,
            housing,
            loan,
            contact,
            day,
            month,
            duration,
            campaign,
            pdays,
            previous,
            poutcome,
            y,
        ]

        generated_df = pd.DataFrame(data, df.columns).T
    else:
        generated_df = df.sample(n=size)

    # save to either csv or db
    if type == "csv":
        curr = strftime("%d-%m-%Y", gmtime())
        os.makedirs("inference", exist_ok=True)
        os.makedirs("inference/input", exist_ok=True)
        dataset_path = f"inference/input/input_{curr}.csv"
        generated_df.to_csv(dataset_path, index=False)
        return dataset_path
    else:
        engine = get_db_connection(database="INFERENCE")
        generated_df.to_sql("INPUT", con=engine, if_exists="replace", index=False)

        return None


if __name__ == "__main__":
    # dev:
    generate_data.fn(size=1000, type="db")
    # generate data everyday, at 2:05 PM IST
    # generate_data.serve(name="generate-data", cron="26 14 * * *")
