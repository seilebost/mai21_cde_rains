import requests
from utils import TestClass


class TestAuthorization(TestClass):
    def test_invalid_header(self):
        res = requests.get(
            f"http://{self.API_ADRESS}:{self.API_PORT}/info",
            headers={"authorization-header": "wrong header"},
        )

        assert res.status_code == 400
        assert res.json() == {"detail": "Invalid authorization header"}

    def test_invalid_b64(self):
        res = requests.get(
            f"http://{self.API_ADRESS}:{self.API_PORT}/info",
            headers={"authorization-header": "Basic wrongb64str"},
        )

        assert res.status_code == 400
        assert res.json() == {"detail": "Invalid base64 string"}

    def test_wrong_user(self):
        res = requests.get(
            f"http://{self.API_ADRESS}:{self.API_PORT}/info",
            headers={"authorization-header": "Basic dXNlcjpwYXNzd29yZA=="},
        )

        assert res.status_code == 403
        assert res.json() == {
            "detail": "You do not have authorization to acces this ressource"
        }

    def test_authorization_score(self):

        res = requests.post(
            f"http://{self.API_ADRESS}:{self.API_PORT}/score",
            headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
            json={"model_name": "SVC"},
        )

        assert res.status_code == 200

    def test_authorization_predict(self):
        upload_file = {
            "file": ("test.csv", open("tests/test.csv", "rb"), "text/csv")
        }

        res = requests.post(
            f"http://{self.API_ADRESS}:{self.API_PORT}/predict/SVC",
            headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
            files=upload_file,
        )

        assert res.status_code == 200
