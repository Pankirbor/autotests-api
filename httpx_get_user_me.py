import httpx


payload = {"email": "leo@list.ru", "password": "1234"}
response = httpx.post("http://localhost:8001/api/v1/authentication/login", json=payload)
token = response.json().get("token").get("accessToken")

response = httpx.get(
    "http://localhost:8001/api/v1/users/me",
    headers={"Authorization": f"Bearer {token}"},
)
print("Ответ сервера с кодом: ", response.status_code)
print(
    "Результат запроса по адресу http://localhost:8001/api/v1/users/me:\n",
    response.json(),
)
