import requests
from api_models import get_models_dict
from train.train import get_processed_data
import pytest
from utils import TestClass

dict_models = get_models_dict()
X_train, X_test, y_train, y_test = get_processed_data()


class TestScores(TestClass):
    @pytest.mark.parametrize("model_name", list(dict_models.keys()))
    def test_score(self, model_name):

        res = requests.post(
            f"http://{self.API_ADRESS}:{self.API_PORT}/score",
            headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
            json={"model_name": model_name},
        )

        assert res.status_code == 200
        assert res.json() == {
            "score": dict_models[model_name].score(X_test, y_test)
        }
