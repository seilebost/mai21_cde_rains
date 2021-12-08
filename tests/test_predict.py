import requests
from api_models import get_models_dict
from train.train import get_processed_data, clean_rows, get_preprocessor
import pytest
import pandas as pd

dict_models = get_models_dict()
X_train, X_test, y_train, y_test = get_processed_data()

test_dataframe = pd.read_csv("tests/test.csv")

test_dataframe = clean_rows(test_dataframe)

X_predict = test_dataframe.drop(["RainTomorrow"], axis=1)

preprocessor = get_preprocessor()

X_predict = preprocessor.transform(X_predict)


@pytest.mark.parametrize("model_name", list(dict_models.keys()))
def test_predict(model_name):

    with open("tests/test.csv", "rb") as csv_file:

        res = requests.post(
            f"http://127.0.0.1:8000/predict/{model_name}",
            headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
            files={"file": ("tests/test.csv", csv_file, "text/csv")},
        )

    assert res.status_code == 200
    assert res.json() == {
        "prediction": dict_models[model_name].predict(X_predict).tolist()
    }


@pytest.mark.parametrize("model_name", list(dict_models.keys()))
def test_predict_wrong_file_type(model_name):

    with open("README.md", "rb") as csv_file:

        res = requests.post(
            f"http://127.0.0.1:8000/predict/{model_name}",
            headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
            files={"file": ("tests/test.csv", csv_file, "text/markdown")},
        )

    assert res.status_code == 400
    assert res.json() == {
        "detail": "Wrong file type or type not specified."
        + "Only csv files are accepted"
    }
