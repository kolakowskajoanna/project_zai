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


# PUT

# PATCH

# DELETE (najpierw se zrob POST(create) a potem to usun)
