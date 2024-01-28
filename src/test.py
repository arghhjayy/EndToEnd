import joblib
import pandas as pd
from preprocess import preprocess
from sklearn.metrics import confusion_matrix, precision_score, recall_score, accuracy_score


def test_model():
    model = joblib.load("artifacts/model.joblib")
    df_test = pd.read_csv("dataset/test.csv")
    y_true = df_test["y"].replace({"yes": 1, "no": 0}).values

    df_test = preprocess(df_test)

    y_pred = model.predict(df_test)

    print(accuracy_score(y_true=y_true, y_pred=y_pred) * 100, "%")
    print(precision_score(y_true=y_true, y_pred=y_pred) * 100)
    print(recall_score(y_true=y_true, y_pred=y_pred) * 100)

    print(confusion_matrix(y_true=y_true, y_pred=y_pred))


if __name__ == "__main__":
    test_model()
