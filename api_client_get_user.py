from clients.client_factory import client_factory, AuthenticationUserDict
from clients.users.public_users_client import CreateUserRequestDict
from tools.fakers import get_random_email

"""Наша цель — написать скрипт, который:

Создаст пользователя через API.
Авторизуется под этим пользователем.
Получит его данные по эндпоинту /api/v1/users/{user_id}.
"""
user_data = {
    "email": get_random_email(),
    "password": "1234",
    "lastName": "Tolstoy",
    "firstName": "Leo",
    "middleName": "none",
}
public_users_client = client_factory.create_public_users_client()

created_user = public_users_client.create_user(CreateUserRequestDict(**user_data))
print("Create user data:", created_user)

private_users_client = client_factory.create_private_users_client(
    AuthenticationUserDict(email=user_data["email"], password=user_data["password"])
)
user = private_users_client.get_user(created_user["user"]["id"])


print("Get user data:", user)
