import requests

response = requests.get("https://api-with-bugs.practicesoftwaretesting.com/products/999/related")
print(response.status_code)
assert response.status_code == 404