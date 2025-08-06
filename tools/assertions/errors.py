from typing import Any

import allure

from clients.errors_schema import ValidationErrorSchema, ValidationErrorResponseSchema
from tools.assertions.base import assert_equal, assert_length


@allure.step("Проверяем данные ожидаемой валидационной ошибки")
def assert_validation_error(
    actual: ValidationErrorSchema, expected: ValidationErrorSchema
) -> None:
    """
    Проверяет соответствие данных валидационной ошибки.

    Args:
        actual (ValidationErrorSchema): Ответ сервера после запроса файла.
        expected (ValidationErrorSchema): Объект ожидаемой ошибки.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    assert_equal(actual.type, expected.type, "type")
    assert_equal(actual.message, expected.message, "message")
    assert_equal(actual.location, expected.location, "location")
    assert_equal(actual.input, expected.input, "input")
    assert_equal(actual.context, expected.context, "context")


@allure.step("Проверяем ответ сервера с ожидаемой валидационной ошибкой")
def assert_validation_error_response(
    actual: ValidationErrorResponseSchema, expected: ValidationErrorResponseSchema
) -> None:
    """
    Проверяет соответствие данных валидационной ошибки.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса файла.
        expected (ValidationErrorResponseSchema): Ожидаемый ответ от сервера с ошибками.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    assert_length(actual.details, expected.details, "details")

    for actual_detail, expected_detail in zip(actual.details, expected.details):
        assert_validation_error(actual_detail, expected_detail)


@allure.step("Проверяем ответ сервера с ожидаемой внутренней ошибкой")
def assert_internal_error_response(actual: Any, expected: Any) -> None:
    """
    Проверяет соответствие данных ошибки.

    Args:
        actual (Any): Ответ сервера после запроса.
        expected (Any): Ожидаемый ответ от сервера с ошибкой.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    assert_equal(actual.details, expected.details, "details"),
