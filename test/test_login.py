import requests, pytest

url = "http://127.0.0.1:5000/login"


@pytest.mark.run(order=2)
def test_valid_login_username_password():

    info = {"username": "ricklanabc", "password": "abcdefgh"}
    response = requests.post(url, json=info)
    assert response.status_code == 200


def test_invalid_login_username():

    info = {"username": "ricklanabc23455", "password": "abcdefgh"}
    response = requests.post(url, json=info)
    assert response.status_code == 404


def test_invalid_login_password():

    info = {"username": "ricklanabc", "password": "abcdefgh234"}
    response = requests.post(url, json=info)
    assert response.status_code == 404


def test_invalid_login_missing_username():

    info = {"password": "abcdefgh234"}
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_login_missing_password():

    info = {"username": "ricklanabc"}
    response = requests.post(url, json=info)
    assert response.status_code == 400
