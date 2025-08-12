import allure

from clients.authentication.authentication_schema import LoginResponseSchema
from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
)
from tools.assertions.base import assert_equal, assert_is_true
from tools.assertions.errors import (
    assert_internal_error_response,
    assert_validation_error_for_invalid_email,
)
from tools.logger import get_logger

logger = get_logger("AUTHENTICATION_ASSERTIONS")


@allure.step("Проверяем ответ сервера после аутентификации")
def assert_login_response(response: LoginResponseSchema) -> None:
    """
    Проверяет структуру ответа на аутентификацию.

    Args:
        response (LoginResponseSchema): Ответ на аутентификацию.

    Raises:
        AssertionError: Если структура ответа не соответствует ожиданиям.
    """

    logger.info("Проверяем ответ сервера после аутентификации")
    assert_equal(response.token.token_type, "bearer", name="token_type")
    assert_is_true(response.token.access_token, "access_token")
    assert_is_true(response.token.refresh_token, "refresh_token")


@allure.step("Проверяем ответ сервера после обновления токена с невалидным токеном")
def assert_refresh_token_with_incorrect_token_response(
    actual: InternalErrorResponseSchema,
) -> None:
    """
    Проверяет ответ сервера после обновления токена с невалидным токеном.

    Args:
        actual (InternalErrorResponseSchema): Ответ сервера после запроса.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    logger.info("Проверяем ответ сервера после обновления токена с невалидным токеном")
    expected = InternalErrorResponseSchema(details="Invalid or expired refresh token")
    assert_internal_error_response(actual=actual, expected=expected)


@allure.step("Проверяем ответ сервера на запрос аутентификации с некорректным email")
def assert_login_with_incorrect_email_response(
    actual: ValidationErrorResponseSchema,
) -> None:
    """
    Проверяет ответ сервера на запрос аутентификации с некорректным email.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    logger.info("Проверяем ответ сервера на запрос аутентификации с некорректным email")
    assert_validation_error_for_invalid_email(actual=actual)
