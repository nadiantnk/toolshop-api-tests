import requests


def test_get_product_returns_200():
    response = requests.get("https://api-with-bugs.practicesoftwaretesting.com/products/1")
    assert response.status_code == 200

def test_related_products_not_found_returns_404():
    response = requests.get("https://api-with-bugs.practicesoftwaretesting.com/products/999/related")
    assert response.status_code == 404

def test_login_returns_200():
    response = requests.post(
        "https://api-with-bugs.practicesoftwaretesting.com/users/login",
        json={
            "email": "customer@practicesoftwaretesting.com",
            "password": "welcome01"
        }
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body

def test_list_brands_200():
    response = requests.get("https://api-with-bugs.practicesoftwaretesting.com/brands")
    assert response.status_code == 200

def test_login_with_invalid_password_401():
    response = requests.post(
        "https://api-with-bugs.practicesoftwaretesting.com/users/login",
        json={
        "email": "customer@practicesoftwaretesting.com",
        "password": "wrongpassword"
        }
    )
    assert response.status_code == 401

def test_new_register_user_201():
    response = requests.post(
        "https://api-with-bugs.practicesoftwaretesting.com/users/register",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "address": "Street 1",
            "city": "City",
            "state": "State",
            "country": "Country",
            "postcode": "1234AA",
            "phone": "0987654321",
            "dob": "1970-01-01",
            "email": "nadi.test.001@example.com",
            "password": "super-secret"
        }
    )
    assert response.status_code == 201
                    