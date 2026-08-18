import pytest
import requests

TIMEOUT = 10


# ---------- products ----------

def test_list_products_returns_200(base_url):
    response = requests.get(f"{base_url}/products", timeout=TIMEOUT)
    assert response.status_code == 200
    assert len(response.json()["data"]) > 0


def test_get_product_by_id_returns_200(base_url):
    products = requests.get(f"{base_url}/products", timeout=TIMEOUT)
    product_id = products.json()["data"][0]["id"]

    response = requests.get(f"{base_url}/products/{product_id}", timeout=TIMEOUT)
    assert response.status_code == 200
    assert response.json()["id"] == product_id


@pytest.mark.xfail(
    strict=True,
    reason="BUG: GET /products/{id}/related с несуществующим id возвращает 500 вместо 404"
)
def test_related_products_not_found_returns_404(base_url):
    response = requests.get(f"{base_url}/products/999/related", timeout=TIMEOUT)
    assert response.status_code == 404


# ---------- brands ----------

def test_list_brands_returns_200(base_url):
    response = requests.get(f"{base_url}/brands", timeout=TIMEOUT)
    assert response.status_code == 200


# ---------- auth ----------

def test_login_returns_200(base_url):
    response = requests.post(
        f"{base_url}/users/login",
        json={
            "email": "customer@practicesoftwaretesting.com",
            "password": "welcome01"
        },
        timeout=TIMEOUT
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_with_invalid_password_returns_401(base_url):
    response = requests.post(
        f"{base_url}/users/login",
        json={
            "email": "customer@practicesoftwaretesting.com",
            "password": "wrongpassword"
        },
        timeout=TIMEOUT
    )
    assert response.status_code == 401


def test_register_returns_201(base_url, user_payload):
    response = requests.post(
        f"{base_url}/users/register",
        json=user_payload,
        timeout=TIMEOUT
    )
    assert response.status_code == 201
    assert "id" in response.json()


def test_users_me_with_token_returns_200(base_url, auth_headers):
    response = requests.get(f"{base_url}/users/me", headers=auth_headers, timeout=TIMEOUT)
    assert response.status_code == 200


def test_users_me_without_token_returns_401(base_url):
    response = requests.get(f"{base_url}/users/me", timeout=TIMEOUT)
    assert response.status_code == 401


# ---------- users: PUT / DELETE ----------

def test_put_update_user_returns_200(base_url, new_user, new_user_headers):
    body = {k: v for k, v in new_user.items() if k not in ("id", "password")}
    body["city"] = "Munich"

    response = requests.put(
        f"{base_url}/users/{new_user['id']}",
        json=body,
        headers=new_user_headers,
        timeout=TIMEOUT
    )
    assert response.status_code == 200


@pytest.mark.xfail(
    strict=True,
    reason="BUG: PUT /users/{id} возвращает 200, но изменения не сохраняются — GET /users/me отдаёт старое значение city"
)
def test_put_update_user_persists_changes(base_url, new_user, new_user_headers):
    body = {k: v for k, v in new_user.items() if k not in ("id", "password")}
    body["city"] = "Munich"

    requests.put(
        f"{base_url}/users/{new_user['id']}",
        json=body,
        headers=new_user_headers,
        timeout=TIMEOUT
    )

    me = requests.get(f"{base_url}/users/me", headers=new_user_headers, timeout=TIMEOUT)
    assert me.json()["city"] == "Munich"


@pytest.mark.xfail(
    strict=True,
    reason="BUG: DELETE /users/{id} владельцем аккаунта возвращает 401 вместо 403"
)
def test_user_cannot_delete_himself_returns_403(base_url, new_user, new_user_headers):
    response = requests.delete(
        f"{base_url}/users/{new_user['id']}",
        headers=new_user_headers,
        timeout=TIMEOUT
    )
    assert response.status_code == 403


def test_delete_user_without_token_returns_401(base_url, new_user):
    response = requests.delete(f"{base_url}/users/{new_user['id']}", timeout=TIMEOUT)
    assert response.status_code == 401


def test_admin_can_delete_user_returns_204(base_url, new_user, admin_headers):
    response = requests.delete(
        f"{base_url}/users/{new_user['id']}",
        headers=admin_headers,
        timeout=TIMEOUT
    )
    assert response.status_code == 204

    login_after = requests.post(
        f"{base_url}/users/login",
        json={"email": new_user["email"], "password": new_user["password"]},
        timeout=TIMEOUT
    )
    assert login_after.status_code == 401