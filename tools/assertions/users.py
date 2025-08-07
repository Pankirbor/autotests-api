import allure

from clients.users.users_schema import (
    CreateUserRequestSchema,
    UserResponseSchema,
    UserSchema,
)
from tools.assertions.base import assert_equal
from tools.logger import get_logger

logger = get_logger("USERS_ASSERTIONS")


@allure.step("Проверяем ответ на запрос создания пользователя")
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
    logger.info("Проверяем ответ на запрос создания пользователя")
    assert_equal(request.email, response.user.email, "email")
    assert_equal(request.first_name, response.user.first_name, "first_name")
    assert_equal(request.last_name, response.user.last_name, "last_name")
    assert_equal(request.middle_name, response.user.middle_name, "middle_name")


@allure.step("Проверяем соответствие данных пользователя")
def assert_user(actual: UserSchema, expected: UserSchema) -> None:
    """
    Проверка соответствия данных пользователя.

    Args:
        actual (UserSchema): Текущие данные пользователя.
        expected (UserSchema): Ожидаемые данные пользователя.

    Raises:
        AssertionError: Если данные не совпадают.
    """
    logger.info("Проверяем соответствие данных пользователя")
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.email, expected.email, "email")
    assert_equal(actual.first_name, expected.first_name, "first_name")
    assert_equal(actual.last_name, expected.last_name, "last_name")
    assert_equal(actual.middle_name, expected.middle_name, "middle_name")


@allure.step("Проверяем ответ сервера на запрос пользователя")
def assert_get_user_response(
    get_user_response: UserResponseSchema, create_user_response: UserResponseSchema
) -> None:
    """
    Проверяет соответствие данных пользователя.
    Args:
        get_user_response (UserResponseSchema): Ответ сервера после запроса пользователя.
        create_user_response (UserResponseSchema): Ответ сервера после создания пользователя.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    logger.info("Проверяем ответ сервера на запрос пользователя")
    assert_user(get_user_response, create_user_response)
