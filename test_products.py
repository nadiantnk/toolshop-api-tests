import pytest
import requests


def test_get_product_returns_200(base_url):
    response = requests.get(f"{base_url}/products/1")
    assert response.status_code == 200


@pytest.mark.xfail(reason="BUG: GET /products/{id}/related с несуществующим id возвращает 500 вместо 404")
def test_related_products_not_found_returns_404(base_url):
    response = requests.get(f"{base_url}/products/999/related")
    assert response.status_code == 404


def test_list_brands_200(base_url):
    response = requests.get(f"{base_url}/brands")
    assert response.status_code == 200


def test_login_returns_200(base_url):
    response = requests.post(
        f"{base_url}/users/login",
        json={
            "email": "customer@practicesoftwaretesting.com",
            "password": "welcome01"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_with_invalid_password_401(base_url):
    response = requests.post(
        f"{base_url}/users/login",
        json={
            "email": "customer@practicesoftwaretesting.com",
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401


def test_new_register_user_201(new_user):
    assert "email" in new_user


def test_users_me_with_token_returns_200(base_url, auth_headers):
    response = requests.get(f"{base_url}/users/me", headers=auth_headers)
    assert response.status_code == 200


def test_put_update_user_200(base_url, new_user):
    login = requests.post(
        f"{base_url}/users/login",
        json={"email": new_user["email"], "password": new_user["password"]}
    )
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    me = requests.get(f"{base_url}/users/me", headers=headers)
    user_id = me.json()["id"]

    new_user["city"] = "Munich"
    response = requests.put(
        f"{base_url}/users/{user_id}",
        json=new_user,
        headers=headers
    )
    assert response.status_code in (200, 204)

@pytest.mark.xfail(reason="BUG: DELETE /users/{id} возвращает 401 вместо 403")
def test_delete_user_returns_403(base_url, new_user):
    login = requests.post(
        f"{base_url}/users/login",
        json={"email": new_user["email"], "password": new_user["password"]}
    )
    headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    me = requests.get(f"{base_url}/users/me", headers=headers)
    user_id = me.json()["id"]

    response = requests.delete(
        f"{base_url}/users/{user_id}",
        headers=headers
    )
    assert response.status_code == 403
