import uuid
import pytest
import requests

BASE_URL = "https://api-with-bugs.practicesoftwaretesting.com"
TIMEOUT = 10


@pytest.fixture
def base_url():
    return BASE_URL


@pytest.fixture
def token(base_url):
    response = requests.post(
        f"{base_url}/users/login",
        json={
            "email": "customer@practicesoftwaretesting.com",
            "password": "welcome01"
        },
        timeout=TIMEOUT
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(base_url):
    response = requests.post(
        f"{base_url}/users/login",
        json={
            "email": "admin@practicesoftwaretesting.com",
            "password": "welcome01"
        },
        timeout=TIMEOUT
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def user_payload():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "address": "Street 1",
        "city": "City",
        "state": "State",
        "country": "Country",
        "postcode": "1234AA",
        "phone": "0987654321",
        "dob": "1970-01-01",
        "email": f"nadi.{uuid.uuid4().hex[:12]}@example.com",
        "password": "super-secret"
    }


@pytest.fixture
def new_user(base_url, user_payload):
    response = requests.post(
        f"{base_url}/users/register",
        json=user_payload,
        timeout=TIMEOUT
    )
    assert response.status_code == 201, f"Регистрация упала: {response.status_code} {response.text}"
    user_payload["id"] = response.json()["id"]
    return user_payload


@pytest.fixture
def new_user_headers(base_url, new_user):
    response = requests.post(
        f"{base_url}/users/login",
        json={"email": new_user["email"], "password": new_user["password"]},
        timeout=TIMEOUT
    )
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}