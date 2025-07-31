from clients.users.users_schema import CreateUserRequestSchema, UserResponseSchema
from tools.assertions.base import assert_equal


def assert_create_user_response(
    request: CreateUserRequestSchema, response: UserResponseSchema
) -> None:
    """
    Проверка ответа на запрос создания пользователя.

    Args:
        request (CreateUserRequestSchema): Отправленные данные для создания пользователя.
        response (UserResponseSchema): Ответ сервера после создания пользователя.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    assert_equal(request.email, response.user.email, "email")
    assert_equal(request.first_name, response.user.first_name, "first_name")
    assert_equal(request.last_name, response.user.last_name, "last_name")
    assert_equal(request.middle_name, response.user.middle_name, "middle_name")
