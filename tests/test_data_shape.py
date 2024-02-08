import os
import sys

sys.path.append(os.path.abspath("."))
os.environ["TESTING"] = "TRUE"


from src.data_classes import DatasetType  # noqa: E402
from src.generate_fake_data import generate_data  # noqa: E402
from src.preprocess import load_and_preprocess  # noqa: E402


def test_shape_train_test():
    assert (
        load_and_preprocess(DatasetType.TEST).shape[1]
        == load_and_preprocess(DatasetType.TRAIN).shape[1]
    )


def test_shape_generated():
    # make a small dataset
    ds_path = generate_data(size=10)
    assert (
        load_and_preprocess(DatasetType.BATCH_INFER).shape[1]
        == load_and_preprocess(DatasetType.TRAIN).shape[1]
    )

    os.remove(ds_path)
