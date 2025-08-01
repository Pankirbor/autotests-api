from typing import Any, Sized

from clients.errors_schema import ValidationErrorSchema, ValidationErrorResponseSchema
from tools.assertions.base import assert_equal


def assert_length(actual: Sized, expected: Sized, name: str) -> None:
    """
    Проверяет соответствие длин коллекций.

    Args:
        actual (Sized): Текущая длина коллекции.
        expected (Sized): Ожидаемая длина коллекции.
        name (str): Название переменной для вывода в сообщении об ошибке.

    Raises:
        AssertionError: Если длины не совпадают.
    """
    assert len(actual) == len(
        expected
    ), f"Incorrect '{name}' length. Expected: '{len(expected)}', resived: '{len(actual)}'"


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
