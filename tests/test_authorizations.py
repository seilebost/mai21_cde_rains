import requests


def test_invalid_header():
    res = requests.get(
        "http://127.0.0.1:8000/info",
        headers={"authorization-header": "wrong header"},
    )

    assert res.status_code == 400
    assert res.json() == {"detail": "Invalid authorization header"}


def test_invalid_b64():
    res = requests.get(
        "http://127.0.0.1:8000/info",
        headers={"authorization-header": "Basic wrongb64str"},
    )

    assert res.status_code == 400
    assert res.json() == {"detail": "Invalid base64 string"}


def test_wrong_user():
    res = requests.get(
        "http://127.0.0.1:8000/info",
        headers={"authorization-header": "Basic dXNlcjpwYXNzd29yZA=="},
    )

    assert res.status_code == 403
    assert res.json() == {
        "detail": "You do not have authorization to acces this ressource"
    }


def test_authorization_score():

    res = requests.post(
        "http://127.0.0.1:8000/score",
        headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
        json={"model_name": "SVC"},
    )

    assert res.status_code == 200


def test_authorization_predict():
    upload_file = {
        "file": ("test.csv", open("tests/test.csv", "rb"), "text/csv")
    }

    res = requests.post(
        "http://127.0.0.1:8000/predict/SVC",
        headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
        files=upload_file,
    )

    assert res.status_code == 200
