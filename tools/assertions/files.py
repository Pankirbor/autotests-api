from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
    ValidationErrorSchema,
)
from clients.files.files_client import FilesClient
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
from tools.assertions.error_builders import ErrorBuilder


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


def assert_create_file_with_empty_field_response(
    actual: ValidationErrorResponseSchema, field: str
):
    """
    Проверяет, что при отправке пустого значения в поле, сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса файла.
        field (str): Имя поля, в котором должен быть пустой строковый параметр.
    """

    expected = ErrorBuilder.create_validation_response(
        ErrorBuilder.string_to_short_error(field_name=field)
    )

    assert_validation_error_response(actual, expected)


def assert_file_not_found_response(actual: InternalErrorResponseSchema):
    """
    Проверяет, что при запросе несуществующего файла сервер возвращает ошибку.

    Args:
        actual (InternalErrorResponseSchema): Ответ сервера после запроса файла.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """

    expected = ErrorBuilder.not_found_error("File")
    assert_internal_error_response(actual, expected)


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

    expected = ErrorBuilder.create_validation_response(
        ErrorBuilder.uuid_parsing_error(
            input_value="incorrect-file-id",
            location=["path", "file_id"],
            error_type="invalid_character",
            char="i",
            position=1,
        )
    )
    assert_validation_error_response(actual, expected)
