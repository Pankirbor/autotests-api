from typing import Any

import allure

from clients.errors_schema import ValidationErrorSchema, ValidationErrorResponseSchema
from tools.assertions.api_error_constants import ErrorContext
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.error_builder import ValidationErrorBuilder
from tools.logger import get_logger


logger = get_logger("ERRORS_ASSSERTIONS")
err_builder = ValidationErrorBuilder()


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

    logger.info("Проверяем данные ожидаемой валидационной ошибки")
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

    logger.info("Проверяем ответ сервера с ожидаемой валидационной ошибкой")

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

    logger.info("Проверяем ответ сервера с ожидаемой внутренней ошибкой")
    assert_equal(actual.details, expected.details, "details"),


@allure.step(
    "Проверяем ответ сервера с ожидаемой валидационной ошибкой с некорректным id"
)
def assert_validation_error_for_invalid_id(
    actual: ValidationErrorResponseSchema,
    location: list[str],
    input_value: str = "incorrect-id",
) -> None:
    """
    Проверяет ошибку валидации для некорректного ID.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса.
        location (str): Место возникновения ошибки (например, "path", "query").
        input_value (str): Некорректное значение ID (по умолчанию "incorrect-id").

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    expected = (
        err_builder.with_input(input_value)
        .with_error(ErrorContext.INVALID_UUID_CHAR, char="i", position=1)
        .at_location(*location)
        .build()
    )
    logger.info(f"Проверяем ошибку валидации для некорректного ID в '{location}'")
    assert_validation_error_response(actual=actual, expected=expected)


@allure.step(
    f"Проверяем ответ сервера с ожидаемой валидационной ошибкой"
    f" для некорректного значения в поле 'email'"
)
def assert_validation_error_for_invalid_email(
    actual: ValidationErrorResponseSchema,
    input_value: str = "",
) -> None:
    err_params = {"err_context": ErrorContext.INVALID_EMAIL, "reason": "@-sign"}
    expected = (
        err_builder.with_input(input_value)
        .with_error(**err_params)
        .at_location("body", "email")
        .build()
    )
    logger.info(
        f"Проверяем ответ сервера с ожидаемой валидационной ошибкой"
        f" для некорректного значения в поле 'email'"
    )
    assert_validation_error_response(actual=actual, expected=expected)


@allure.step(
    f"Проверяем ответ сервера с ожидаемой валидационной ошибкой"
    f" на пустое обязательное поле c id {{field_name}} в теле запроса"
)
def assert_validation_error_for_empty_id_field(
    actual: ValidationErrorResponseSchema,
    field_name: str,
) -> None:
    err_params = {"err_context": ErrorContext.INVALID_UUID_LENGTH, "length": 0}
    expected = (
        err_builder.with_input("")
        .with_error(**err_params)
        .at_location("body", field_name)
        .build()
    )
    logger.info(
        f"Проверям ошибку валидации для отсутствующего значения в поле '{field_name}'"
    )
    assert_validation_error_response(actual=actual, expected=expected)


@allure.step(
    f"Проверяем ответ сервера с ожидаемой валидационной ошибкой"
    f" на пустое обязательное стоковое поле {{field_name}} в теле запроса"
)
def assert_validation_error_for_empty_string_field(
    actual: ValidationErrorResponseSchema,
    field_name: str,
) -> None:
    err_params = {"err_context": ErrorContext.STRING_TOO_SHORT, "min_length": 1}

    expected = (
        err_builder.with_input("")
        .with_error(**err_params)
        .at_location("body", field_name)
        .build()
    )
    logger.info(
        f"Проверям ошибку валидации для отсутствующего значения в поле '{field_name}'"
    )
    assert_validation_error_response(actual=actual, expected=expected)


@allure.step(
    f"Проверяем ответ сервера с ожидаемой валидационной ошибкой"
    f" для значения, превышающего максимальную длину поля {{location}} в теле запроса"
)
def assert_validation_error_for_too_long_field(
    actual: ValidationErrorResponseSchema,
    location: str,
    input_value: str,
    max_length: int,
) -> None:
    error_params = {
        "err_context": ErrorContext.STRING_TOO_LONG,
        "max_length": max_length,
    }

    expected = (
        err_builder.with_input(input_value)
        .with_error(**error_params)
        .at_location("body", location)
        .build()
    )
    logger.info(
        f"Проверям ошибку валидации для значения,"
        f" превышающего максимальную длину поля '{location}'"
    )
    assert_validation_error_response(actual, expected)
