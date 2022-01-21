import requests, pytest

url = "http://127.0.0.1:5000/api/deleteTask"


def test_valid_deleteTask():

    info = {"taskID": "1"}
    response = requests.delete(url, params=info)
    assert response.status_code == 200


def test_invalid_deleteTask_missing_taskID():

    info = {"title": "Test1", "description": "This is a test", "priority": "H"}
    response = requests.delete(url, params=info)
    assert response.status_code == 400


def test_invalid_deleteTask_invalid_taskID():

    info = {"taskID": "abc"}
    response = requests.delete(url, params=info)
    assert response.status_code == 404

