from http import HTTPStatus
import pytest

from clients.files.files_client import FilesClient
from clients.files.files_schema import UploadFileRequestSchema, UploadFileResponseSchema
from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
)
from fixtures.files import FileFixture
from tools.assertions.base import assert_status_code
from tools.assertions.files import (
    assert_create_file_with_empty_field_response,
    assert_file_is_accessible,
    assert_file_not_found_response,
    assert_get_file_with_incorrect_file_id_response,
    assert_upload_file_response,
    assert_get_file_response,
)
from tools.assertions.schema import validate_json_schema


@pytest.mark.files
@pytest.mark.regression
class TestFiles:

    def test_upload_file(self, files_client: FilesClient):
        """
        Тест проверяет, что при загрузке файла на сервер,
        в ответе сервера возвращается информация о файле.

        Args:
            files_client (FilesClient): HTTP-клиент для взаимодействия с сервером.

        Raises:
            AssertionError: Если данные в ответе не совпадают с ожидаемыми.
        """

        request = UploadFileRequestSchema(upload_file="./testdata/files/image.jpg")
        response = files_client.upload_file_api(request)
        response_data = UploadFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_upload_file_response(request=request, response=response_data)
        assert_file_is_accessible(files_client, response_data.file.id, HTTPStatus.OK)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_get_file(self, files_client: FilesClient, function_file: FileFixture):
        """
        Тест проверяет, что при запросе файла по его идентификатору,
        в ответе сервера возвращается информация о файле.

        Args:
            files_client (FilesClient): HTTP-клиент для взаимодействия с сервером.
            function_file (FileFixture): Объект с данными загруженного файла.

        Raises:
            AssertionError: Если данные в ответе не совпадают с ожидаемыми.
        """

        response = files_client.get_file_api(function_file.file_id)
        response_data = UploadFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_file_response(response_data, function_file.response)

        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_file(self):
        pass

    @pytest.mark.parametrize("field_name", ["filename", "directory"])
    def test_upload_file_with_missing_request_field(
        self, field_name: str, files_client: FilesClient
    ):
        """
        Тест проверяет, что при отправке запроса с пустым полем в request,
        в ответе сервера возвращается ошибка валидации.

        Args:
            field_name (str): Имя поля, которое будет пустым в запросе.
            files_client (FilesClient): HTTP-клиент для взаимодействия с сервером.

        Raises:
            AssertionError: Если данные в ответе не совпадают с ожидаемыми.
        """

        request = UploadFileRequestSchema(upload_file="./testdata/files/image.jpg")
        setattr(request, field_name, "")
        response = files_client.upload_file_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_file_with_empty_field_response(response_data, field_name)
        validate_json_schema(response.json(), response_data.model_json_schema())

    def test_delete_file(self, files_client: FilesClient, function_file: FileFixture):
        """
        Тест проверяет, что при удалении файла,
        он удаляется из хранилища и не может быть получен по его идентификатору.

        Args:
            files_client (FilesClient): HTTP-клиент для взаимодействия с сервером.
            function_file (FileFixture): Объект с данными загруженного файла.

        Raises:
            AssertionError: Если данные в ответе не совпадают с ожидаемыми.
        """

        delete_response = files_client.delete_file_api(function_file.file_id)

        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = files_client.get_file_api(function_file.file_id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(
            get_response.text
        )

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_file_not_found_response(get_response_data)

        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

    def test_get_file_with_incorrect_file_id(self, files_client: FilesClient):
        """
        Тест проверяет, что при запросе несуществующего файла,
        в ответе сервера возвращается ошибка.

        Args:
            files_client (FilesClient): HTTP-клиент для взаимодействия с сервером.

        Raises:
            AssertionError: Если данные в ответе не совпадают с ожидаемыми.
        """
        response = files_client.get_file_api("incorrect-file-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_file_with_incorrect_file_id_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())
