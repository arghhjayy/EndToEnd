import os
import sys

sys.path.append(os.path.abspath("."))
os.environ["TESTING"] = "TRUE"


from src.preprocess import load_and_preprocess  # noqa: E402


def test_shape():
    assert (
        load_and_preprocess("test").shape[1]
        == load_and_preprocess("train").shape[1]
    )


test_shape()
