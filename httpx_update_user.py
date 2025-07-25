import httpx

from tools.api_routes import APIRoutes
from tools.fakers import get_random_email

user_create_data = {
    "email": get_random_email(),
    "password": "1234",
    "lastName": "Tolstoy",
    "firstName": "Leo",
    "middleName": "none",
}

user_login_data = {
    "email": user_create_data["email"],
    "password": user_create_data["password"],
}
user_update_data = {
    "email": get_random_email(),
    "lastName": "Tolstoy",
    "firstName": "Leo",
    "middleName": "none",
}


def get_token(client: httpx.Client, user_data: str | dict[str, str]) -> dict[str, str]:
    response = client.post(APIRoutes.AUTHENTICATION.join_path("login"), json=user_data)
    print("Статус код запроса на получение токена:\n", response.status_code, end="\n\n")
    if response.is_success:
        token = response.json()["token"]["accessToken"]
        refresh = response.json()["token"]["refreshToken"]
        return token, refresh


with httpx.Client() as client:
    response = client.post(
        APIRoutes.USERS.join_path("", delimitr=""), json=user_create_data
    )
    print("Статус код запроса на создание пользователя:\n", response.status_code)
    user = response.json()["user"]
    print("Данные от сервера:\n", user, end="\n\n")

    token, refresh_token = get_token(client, user_login_data)
    if token:
        client.headers = {"Authorization": f"Bearer {token}"}
        response_update = client.patch(
            APIRoutes.USERS.join_path(str(user["id"])), json=user_update_data
        )
        print(
            "Статус код запроса на изменение пользователя:\n",
            response_update.status_code,
        )
        print("Данные от сервера:\n", response_update.json(), end="\n\n")
