import requests


def test_api_status():
    res = requests.get("http://127.0.0.1:8000")

    assert res.status_code == 200
    assert res.json() == {"status": "running"}


def test_api_info():
    res = requests.get(
        "http://127.0.0.1:8000/info",
        headers={"authorization-header": "Basic YWxpY2U6d29uZGVybGFuZA=="},
    )

    assert res.status_code == 200
