import requests
from api_models import get_models_list
from utils import TestClass


class TestUnit(TestClass):
    def test_api_status(self):
        res = requests.get(f"http://{self.API_ADRESS}:{self.API_PORT}")

        assert res.status_code == 200
        assert res.json() == {"status": "running"}

    def test_api_info(self):
        res = requests.get(
            f"http://{self.API_ADRESS}:{self.API_PORT}/info",
            headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
        )

        assert res.status_code == 200
        assert res.json() == {"models": get_models_list()}
