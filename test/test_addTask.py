import requests, pytest

url = "http://127.0.0.1:5000/api/addTask"


@pytest.mark.run(order=3)
def test_valid_addTask():

    info = {
        "username": "ricklanabc",
        "title": "Test1",
        "description": "This is a test",
        "priority": "H",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 200


def test_invalid_addTask_missing_username():

    info = {"title": "Test1", "description": "This is a test", "priority": "H"}
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_addTask_missing_title():

    info = {"username": "ricklanabc", "description": "This is a test", "priority": "H"}
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_addTask_missing_description():

    info = {"username": "ricklanabc", "title": "Test1", "priority": "H"}
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_addTask_missing_priority():

    info = {"username": "ricklanabc", "title": "Test1", "description": "This is a test"}
    response = requests.post(url, json=info)
    assert response.status_code == 400


def test_invalid_addTask_nonexistent_username():

    info = {
        "username": "ricklanabc123456789",
        "title": "Test1",
        "description": "This is a test",
        "priority": "H",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 404


def test_invalid_addTask_nonexistent_priority_low():

    info = {
        "username": "ricklanabc",
        "title": "Test1",
        "description": "This is a test",
        "priority": "l",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 404


def test_invalid_addTask_nonexistent_priority_medium():

    info = {
        "username": "ricklanabc",
        "title": "Test1",
        "description": "This is a test",
        "priority": "m",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 404


def test_invalid_addTask_nonexistent_priority_high():

    info = {
        "username": "ricklanabc",
        "title": "Test1",
        "description": "This is a test",
        "priority": "h",
    }
    response = requests.post(url, json=info)
    assert response.status_code == 404
