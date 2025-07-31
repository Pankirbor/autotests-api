from http import HTTPStatus

import pytest

from clients.users.public_users_client import PublicUsersClient
from clients.users.private_users_client import PrivateUsersClient
from clients.users.users_schema import CreateUserRequestSchema, UserResponseSchema
from fixtures.users import UserFixture
from tools.assertions.schema import validate_json_schema
from tools.assertions.base import assert_status_code
from tools.assertions.users import assert_create_user_response, assert_get_user_response
from tools.fakers import fake


@pytest.mark.regression
@pytest.mark.users
@pytest.mark.parametrize("email", ["gmail.com", "mail.ru", "example.com"])
def test_create_user(public_users_client: PublicUsersClient, email: str):
    """Тест создания пользователя.

    Args:
        public_users_client (PublicUsersClient): Клиент для работы с публичными users эндпоинтами API.

    Raises:
        AssertionError: Если статус код ответа не равен HTTPStatus.OK.
        ValidationError: Если данные ответа не соответствуют схеме.
    """

    request = CreateUserRequestSchema(email=fake.email(email))
    response = public_users_client.create_user_api(request)
    response_data = UserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_create_user_response(request, response_data)

    validate_json_schema(response.json(), response_data.model_json_schema())


@pytest.mark.regression
@pytest.mark.users
def test_get_user_me(
    private_users_client: PrivateUsersClient, function_user: UserFixture
):
    """
    Тест получения информации о пользователе по url users/me.

    Args:
        private_users_client (PrivateUsersClient): Клиент для работы с закрытыми users эндпоинтами API.
        function_user (UserFixture): Объект с данными созданного пользователя.

    Raises:
        AssertionError: Если статус код ответа не равен HTTPStatus.OK.
        ValidationError: Если данные ответа не соответствуют схеме.
    """
    response = private_users_client.get_user_me_api()
    response_data = UserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_get_user_response(response_data.user, function_user.response.user)

    validate_json_schema(response.json(), response_data.model_json_schema())
