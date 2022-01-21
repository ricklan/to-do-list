import requests, pytest, os

url = "http://127.0.0.1:5000/signup"


@pytest.mark.run(order=1)
def test_valid_signup_all_strings():

    info = {
        "username": "ricklanabc",
        "password": "abcdefgh",
        "firstname": "rick",
        "lastname": "lan",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 200


def test_valid_signup_string_and_numbers():
    info = {
        "username": "ricklan1234",
        "password": "abcdefgh5678",
        "firstname": "rick",
        "lastname": "lan",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 200


def test_invalid_signup_username_symbols():
    info = {
        "username": "ricklan@#$",
        "password": "abcdefgh5678",
        "firstname": "rick",
        "lastname": "lan",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_signup_username_length():
    info = {
        "username": "ricklan",
        "password": "abcdefgh5678",
        "firstname": "rick",
        "lastname": "lan",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_signup_username_duplicate():
    info = {
        "username": "ricklanabc",
        "password": "abcdefgh5678",
        "firstname": "rick",
        "lastname": "lan",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_signup_password_symbols():
    info = {
        "username": "ricklan1",
        "password": "abcdefgh5678@!#$%",
        "firstname": "rick",
        "lastname": "lan",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_signup_password_length():
    info = {
        "username": "ricklan1",
        "password": "abcd",
        "firstname": "rick",
        "lastname": "lan",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_signup_firstname_symbol_number():
    info = {
        "username": "ricklan1",
        "password": "abcdefghjk",
        "firstname": "rick!@#123",
        "lastname": "lan",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_signup_firstname_length():
    info = {
        "username": "ricklan1",
        "password": "abcdefghjk",
        "firstname": "",
        "lastname": "lan",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_signup_lastname_symbol_number():
    info = {
        "username": "ricklan1",
        "password": "abcdefghjk",
        "firstname": "rick",
        "lastname": "lan12#$%",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_signup_lastname_length():
    info = {
        "username": "ricklan1",
        "password": "abcdefghjk",
        "firstname": "rick",
        "lastname": "",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_signup_missing_username():
    info = {"password": "abcdefghjk", "firstname": "rick", "lastname": ""}
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_signup_missing_password():
    info = {"username": "ricklan1", "firstname": "rick", "lastname": ""}
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_signup_missing_firstname():
    info = {"username": "ricklan1", "password": "abcdefghjk", "lastname": ""}
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_signup_missing_lastname():
    info = {"username": "ricklan1", "password": "abcdefghjk", "firstname": "rick"}
    response = requests.post(url, json=info)
    assert response.status_code == 400

