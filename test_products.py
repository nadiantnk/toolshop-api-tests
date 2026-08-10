import requests


def test_get_product_returns_200():
    response = requests.get("https://api-with-bugs.practicesoftwaretesting.com/products/1")
    assert response.status_code == 200

def test_related_products_not_found_returns_404():
    response = requests.get("https://api-with-bugs.practicesoftwaretesting.com/products/999/related")
    assert response.status_code == 404