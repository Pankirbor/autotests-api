import allure

from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
    ValidationErrorSchema,
)
from clients.files.files_schema import (
    FileSchema,
    UploadFileRequestSchema,
    UploadFileResponseSchema,
)
from tools.assertions.base import assert_equal, assert_status_code
from tools.assertions.errors import (
    assert_internal_error_response,
    assert_validation_error_response,
)
from clients.files.files_client import FilesClient


@allure.step("Проверяем ответ сервера после загрузки файла")
def assert_upload_file_response(
    request: UploadFileRequestSchema, response: UploadFileResponseSchema
):
    """
    Проверка ответа на запрос загрузки файла.

    Args:
        request (UploadFileRequestSchema): Отправленные данные для загрузки файла.
        response (UploadFileResponseSchema): Ответ сервера после загрузки файла.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """

    expected_url = (
        f"http://localhost:8000/static/{request.directory}/{request.filename}"
    )
    assert_equal(response.file.filename, request.filename, "filename")
    assert_equal(response.file.directory, request.directory, "directory")
    assert_equal(str(response.file.url), expected_url, "url")


@allure.step("Проверяем доступность файла по URL")
def assert_file_is_accessible(
    client: FilesClient, file_id: str, expected_status_code: int
):
    """
    Проверяет, что файл доступен по указанному URL.

    Args:
        client (FilesClient): HTTP-клиент для взаимодействия с сервером.
        url (str): URL, по которому должен быть доступен файл.
        expected_status_code (int): Ожидаемый HTTP-код ответа.

    Raises:
        AssertionError: Если статус код ответа не соответствует ожидаемому.
    """

    response = client.get_file_api(file_id)
    assert_status_code(response.status_code, expected_status_code)


@allure.step("Проверяем соответствие данных файла")
def assert_file(actual: FileSchema, expected: FileSchema):
    """
    Проверяет соответствие данных файла.

    Args:
        actual (FileSchema): Текущие данные файла.
        expected (FileSchema): Ожидаемые данные файла.

    Raises:
        AssertionError: Если данные не совпадают.
    """

    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.filename, expected.filename, "filename")
    assert_equal(actual.directory, expected.directory, "directory")
    assert_equal(actual.url, expected.url, "url")


@allure.step("Проверяем ответ сервера на запрос файла")
def assert_get_file_response(
    get_file_response: UploadFileResponseSchema,
    create_file_response: UploadFileResponseSchema,
) -> None:
    """
    Проверяет соответствие данных файла.

    Args:
        get_file_response (UploadFileResponseSchema): Ответ сервера после запроса файла.
        create_file_response (UploadFileResponseSchema): Ответ сервера после создания файла.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """

    assert_file(get_file_response.file, create_file_response.file)


@allure.step("Проверяем ответ сервера на запрос создания файла с пустым полем")
def assert_create_file_with_empty_field_response(
    actual: ValidationErrorResponseSchema, field: str
):
    """
    Проверяет, что при отправке пустого значения в поле, сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса файла.
        field (str): Имя поля, в котором должен быть пустой строковый параметр.
    """

    expected = ValidationErrorResponseSchema(
        detail=[
            ValidationErrorSchema(
                type="string_too_short",
                input="",
                context={"min_length": 1},
                message="String should have at least 1 character",
                location=["body", field],
            )
        ]
    )

    assert_validation_error_response(actual, expected)


@allure.step("Проверяем ответ сервера на запрос несуществующего файла")
def assert_file_not_found_response(actual: InternalErrorResponseSchema):
    """
    Проверяет, что при запросе несуществующего файла сервер возвращает ошибку.

    Args:
        actual (InternalErrorResponseSchema): Ответ сервера после запроса файла.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """

    expected = InternalErrorResponseSchema(details="File not found")
    assert_internal_error_response(actual, expected)


@allure.step("Проверяем ответ сервера на запрос файла с некорректным id")
def assert_get_file_with_incorrect_file_id_response(
    actual: ValidationErrorResponseSchema,
):
    """
    Проверяет, что при запросе несуществующего файла сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса файла.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """

    context_error_val = (
        f"invalid character: expected an optional prefix of "
        f"`urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"
    )
    msg = f"Input should be a valid UUID, {context_error_val}"
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect-file-id",
                context={"error": context_error_val},
                message=msg,
                loc=["path", "file_id"],
            )
        ]
    )
    assert_validation_error_response(actual, expected)
