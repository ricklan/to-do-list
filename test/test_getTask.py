import requests, pytest

url = "http://127.0.0.1:5000/api/getTask"


@pytest.mark.run(order=4)
def test_valid_getTask():

    info = {"username": "ricklanabc", "pageNumber": "1", "filter": "H"}
    response = requests.get(url, params=info)
    result = [
        {
            "description": "This is a test",
            "priority": "H",
            "taskID": 1,
            "title": "Test1",
            "totalNumPages": 1,
        }
    ]
    assert response.status_code == 200 and response.json() == result


def test_invalid_getTask_missing_username():

    info = {"pageNumber": "1", "filter": "H"}
    response = requests.get(url, params=info)
    assert response.status_code == 400


def test_invalid_getTask_missing_pageNumber():

    info = {"username": "ricklanabc", "filter": "H"}
    response = requests.get(url, params=info)
    assert response.status_code == 400


def test_invalid_getTask_missing_filter():

    info = {"username": "ricklanabc", "pageNumber": "1"}
    response = requests.get(url, params=info)
    assert response.status_code == 200


def test_invalid_getTask_invalid_pageNumber_1():

    info = {"username": "ricklanabc", "pageNumber": "0", "filter": "H"}
    response = requests.get(url, params=info)
    assert response.status_code == 400


def test_invalid_getTask_invalid_pageNumber_2():

    info = {"username": "ricklanabc", "pageNumber": "abc", "filter": "H"}
    response = requests.get(url, params=info)
    assert response.status_code == 400

