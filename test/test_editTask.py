import requests, pytest

url = "http://127.0.0.1:5000/api/editTask"


@pytest.mark.run(order=5)
def test_valid_editTask():

    info = {
        "taskID": "1",
        "title": "Test1",
        "description": "This is a test",
        "priority": "H",
    }
    response = requests.patch(url, json=info)
    assert response.status_code == 200


def test_invalid_editTask_missing_taskID():

    info = {"title": "Test1", "description": "This is a test", "priority": "H"}
    response = requests.patch(url, json=info)
    assert response.status_code == 400


def test_invalid_editTask_missing_title():

    info = {"taskID": "1", "description": "This is a test", "priority": "H"}
    response = requests.patch(url, json=info)
    assert response.status_code == 400


def test_invalid_editTask_missing_description():

    info = {"taskID": "1", "title": "Test1", "priority": "H"}
    response = requests.patch(url, json=info)
    assert response.status_code == 400


def test_invalid_editTask_missing_priority():

    info = {"taskID": "1", "title": "Test1", "description": "This is a test"}
    response = requests.patch(url, json=info)
    assert response.status_code == 400


def test_invalid_editTask_nonexistent_taskID():

    info = {
        "taskID": "abc",
        "title": "Test1",
        "description": "This is a test",
        "priority": "H",
    }
    response = requests.patch(url, json=info)
    assert response.status_code == 404


def test_invalid_editTask_nonexistent_priority_low():

    info = {
        "taskID": "ricklanabc",
        "title": "Test1",
        "description": "This is a test",
        "priority": "l",
    }
    response = requests.patch(url, json=info)
    assert response.status_code == 404


def test_invalid_editTask_nonexistent_priority_medium():

    info = {
        "taskID": "ricklanabc",
        "title": "Test1",
        "description": "This is a test",
        "priority": "m",
    }
    response = requests.patch(url, json=info)
    assert response.status_code == 404


def test_invalid_editTask_nonexistent_priority_high():

    info = {
        "taskID": "ricklanabc",
        "title": "Test1",
        "description": "This is a test",
        "priority": "h",
    }
    response = requests.patch(url, json=info)
    assert response.status_code == 404
