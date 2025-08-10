import allure

from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
)
from clients.users.constants import MAX_LENGTH_FIELDS, FIELD_NAME_MAPPING
from clients.users.users_schema import (
    CreateUserRequestSchema,
    UpdateUserRequestSchema,
    UserResponseSchema,
    UserSchema,
)
from tools.assertions.base import assert_equal
from tools.assertions.api_error_constants import ErrorContext
from tools.assertions.errors import (
    assert_internal_error_response,
    assert_validation_error_response,
)
from tools.assertions.error_builder import ValidationErrorBuilder
from tools.logger import get_logger

logger = get_logger("USERS_ASSERTIONS")
err_builder = ValidationErrorBuilder()


def assert_validation_error_for_invalid_id(
    actual: ValidationErrorResponseSchema,
    location: str,
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
        .at_location(location, "user_id")
        .build()
    )
    logger.info(f"Проверяем ошибку валидации для некорректного ID в {location}")
    assert_validation_error_response(actual=actual, expected=expected)


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


@allure.step("Проверяем ответ на запрос обновления данных пользователя")
def assert_update_user_response(
    actual: UserResponseSchema,
    expected: UpdateUserRequestSchema,
    user_id: str,
) -> None:
    """
    Проверка ответа на запрос обновления данных пользователя.

    Args:
        request (UpdateUserRequestSchema): Отправленные данные для обновления.
        response (UserResponseSchema): Ответ сервера после обновления.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    logger.info("Проверяем ответ на запрос обновления данных пользователя")
    assert_equal(user_id, actual.user.id, "id")
    assert_equal(expected.email, actual.user.email, "email")
    assert_equal(expected.first_name, actual.user.first_name, "first_name")
    assert_equal(expected.last_name, actual.user.last_name, "last_name")
    assert_equal(expected.middle_name, actual.user.middle_name, "middle_name")


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


@allure.step(
    f"Проверям ответ сервера после запроса на создание "
    f"или обновление пользователя с пустым обязательным параметром."
)
def assert_create_or_update_user_with_empty_required_field_response(
    actual: ValidationErrorResponseSchema, field_name: str
) -> None:
    """
    Проверяет ответ сервера после запроса на создание или обновление пользователя
    с пустым обязательным параметром.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса.
        field_name (str): Имя поля, в котором должен быть пустой строковый параметр.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    if field_name == "email":
        error_params = {"err_context": ErrorContext.INVALID_EMAIL, "reason": "@-sign"}
    else:
        error_params = {"err_context": ErrorContext.STRING_TOO_SHORT, "min_length": 1}

    expected = (
        err_builder.with_input("")
        .with_error(**error_params)
        .at_location("body", FIELD_NAME_MAPPING.get(field_name))
        .build()
    )
    logger.info(
        f"Проверям ответ сервера после запроса на создание "
        f"или обновление пользователя с пустым обязательным параметром."
    )
    assert_validation_error_response(actual, expected)


@allure.step(
    f"Проверям ответ сервера после запроса на создание "
    f"или обновление пользователя со значением, превышающим максимальную длину поля."
)
def assert_create_or_update_user_with_too_long_field_response(
    actual: ValidationErrorResponseSchema,
    input_val: str,
    field_name: str,
) -> None:
    """
    Проверяет ответ сервера после запроса на создание или обновление пользователя
    со значением, превышающим максимальную длину поля.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса.
        input_val (str): Значение, которое должно быть отправлено в поле.
        field_name (str): Имя поля, в котором должен быть слишком длинный строковый параметр.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    if field_name == "email":
        error_params = {"err_context": ErrorContext.INVALID_EMAIL, "reason": "@-sign"}
    else:
        error_params = {
            "err_context": ErrorContext.STRING_TOO_LONG,
            "max_length": MAX_LENGTH_FIELDS.get(field_name),
        }

    expected = (
        err_builder.with_input(input_val)
        .with_error(**error_params)
        .at_location("body", FIELD_NAME_MAPPING.get(field_name))
        .build()
    )
    logger.info(
        f"Проверям ответ сервера после запроса на создание "
        f"или обновление пользователя со значением, превышающим максимальную длину поля."
    )
    assert_validation_error_response(actual, expected)


@allure.step(
    "Проверяем ответ сервера на запрос удаления пользователя с некорректным id"
)
def assert_delete_user_with_incorrect_user_id_response(
    actual: ValidationErrorResponseSchema,
) -> None:
    """
    Проверяет, что при запросе удаления пользователя с некорректным id сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """

    logger.info(
        "Проверяем ответ сервера на запрос удаления пользователя с некорректным id"
    )
    assert_validation_error_for_invalid_id(actual=actual, location="path")


def assert_get_user_with_incorrect_user_id_response(
    actual: ValidationErrorResponseSchema,
) -> None:
    """
    Проверяет, что при запросе пользователя с некорректным id сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    logger.info("Проверяем ответ сервера на запрос пользователя с некорректным id")
    assert_validation_error_for_invalid_id(actual=actual, location="path")


@allure.step("Проверяем ответ сервера на запрос несуществующего пользователя")
def assert_not_found_user_response(actual: InternalErrorResponseSchema):
    """
    Проверяет, что при запросе несуществующего пользователя сервер возвращает ошибку.

    Args:
        actual (InternalErrorResponseSchema): Ответ сервера после запроса пользователя.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """

    expected = InternalErrorResponseSchema(details="User not found")
    logger.info("Проверяем ответ сервера на запрос несуществующего пользователя")
    assert_internal_error_response(actual=actual, expected=expected)
