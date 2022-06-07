import requests

API_URL = "http://127.0.0.1:8000/api"

ADMIN = {
    "username": "admin",
    "password": "admin"
}

EMPLOYEE = {
    "username": "emp",
    "password": "emp"
}

DOGGO = {
    "name": "kropek",
    "age": 18,
    "sex": "M"
}


def get_jwt(user) -> str:
    r = requests.post(f"{API_URL}/token", json={
        "username": user["username"],
        "password": user["password"]
    })
    assert r.status_code == 200
    return r.json()["access"]


def test_admin_token():
    """
    POST na token dla admina
    """
    token = get_jwt(ADMIN)
    assert token is not None


def test_list_groups_as_admin():
    """
    GET na grupy jako admin powinien oddac 200 + application/json
    """
    token = get_jwt(ADMIN)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = requests.get(f"{API_URL}/groups", headers=headers)
    assert r.status_code == 200
    assert "employees" in [g["name"] for g in r.json()["results"]]
    assert "application/json" == r.headers.get("Content-Type")


def test_list_groups_as_non_admin():
    """
    GET na grupy jako non admin powinien oddac 403
    """
    token = get_jwt(EMPLOYEE)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    r = requests.get(f"{API_URL}/groups", headers=headers)
    assert r.status_code == 403


def test_add_and_delete_puppy_as_adm():
    """
    POST puppy jako admin -> success
    and
    DELETE puppy jako administrator
    """
    token = get_jwt(ADMIN)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    body = {
        "name": DOGGO.get("name"),
        "age": DOGGO.get("age"),
        "sex": DOGGO.get("sex"),
        "adoption": None
    }
    r = requests.post(f"{API_URL}/puppys", headers=headers, json=body)
    assert r.status_code == 201
    assert "application/json" == r.headers.get("Content-Type")

    # -- clean after test
    
    doggo_id = r.json().get('id')
    r = requests.delete(f"{API_URL}/puppys/{doggo_id}", headers=headers)
    assert r.status_code == 204


def test_update_puppy_as_adm():
    """
    PATCH puppy name, jako admin -> powinno oddać 201 i name powinien sie zmienic
    """
    token = get_jwt(ADMIN)
    # -- setup for test
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    body = {
        "name": DOGGO.get("name"),
        "age": DOGGO.get("age"),
        "sex": DOGGO.get("sex"),
        "adoption": None
    }
    r = requests.post(f"{API_URL}/puppys", headers=headers, json=body)
    assert r.status_code == 201
    assert "application/json" == r.headers.get("Content-Type")

    # -- test
    doggo_id = r.json().get('id')
    r = requests.patch(f"{API_URL}/puppys/{doggo_id}", json={"name": "coco"}, headers=headers)
    assert r.status_code == 200
    assert r.json().get("name") == "coco"

    # -- clean after test
    r = requests.delete(f"{API_URL}/puppys/{doggo_id}", headers=headers )
    assert r.status_code == 204
