import os

import pandas as pd
from flask import Flask, jsonify, request
from mlflow.sklearn import load_model

from preprocess import preprocess

app = Flask(__name__)


@app.route("/infer", methods=["POST"])
def infer():
    model = load_model("model_dir")

    data = request.get_json()

    df = pd.DataFrame(data.values(), index=data.keys()).T

    print(df.head())

    df = preprocess.fn(df)

    pred = model.predict(df)

    return jsonify({"prediction": int(pred[0])})


if __name__ == "__main__":
    os.environ["TESTING"] = "TRUE"
    app.run(debug=True)
