import requests
from api_models import get_models_dict, get_data
import pytest

dict_models = get_models_dict()
X_train, X_test, y_train, y_test = get_data()


@pytest.mark.parametrize("model_name", list(dict_models.keys()))
def test_score(model_name):

    res = requests.post(
        "http://127.0.0.1:8000/score",
        headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
        json={"model_name": model_name},
    )

    assert res.status_code == 200
    assert res.json() == {
        "score": dict_models[model_name].score(X_test, y_test)
    }
