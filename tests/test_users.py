from http import HTTPStatus

import pytest

from clients.users.public_users_client import get_public_users_client
from clients.users.users_schema import CreateUserRequestSchema, UserResponseSchema
from tools.assertions.schema import validate_json_schema
from tools.assertions.base import assert_status_code
from tools.assertions.users import assert_create_user_response


def test_create_user():
    """Тест создания пользователя."""

    public_users_client = get_public_users_client()
    user_request = CreateUserRequestSchema()
    response = public_users_client.create_user_api(user_request)
    created_user = UserResponseSchema.model_validate_json(response.text)

    assert_status_code(response.status_code, HTTPStatus.OK)
    assert_create_user_response(user_request, created_user)

    validate_json_schema(response.json(), created_user.model_json_schema())
