import allure

from clients.authentication.authentication_schema import LoginResponseSchema
from tools.assertions.base import assert_equal, assert_is_true
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
