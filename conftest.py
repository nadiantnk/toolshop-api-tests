import pytest
import requests
import random


@pytest.fixture
def base_url():
    return "https://api-with-bugs.practicesoftwaretesting.com"


@pytest.fixture
def token(base_url):
    response = requests.post(
        base_url + "/users/login",
        json={
            "email": "customer@practicesoftwaretesting.com",
            "password": "welcome01"
        }
    )
    return response.json()["access_token"]


@pytest.fixture
def auth_headers(token):
    return {"Authorization": "Bearer " + token}


@pytest.fixture
def new_user(base_url):
    email = "nadi." + str(random.randint(1000, 9999)) + "@example.com"
    payload = {
        "first_name": "John",
        "last_name": "Doe",
        "address": "Street 1",
        "city": "City",
        "state": "State",
        "country": "Country",
        "postcode": "1234AA",
        "phone": "0987654321",
        "dob": "1970-01-01",
        "email": email,
        "password": "super-secret"
    }
    requests.post(base_url + "/users/register", json=payload)
    return payload