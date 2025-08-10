from http import HTTPStatus

import allure
from allure_commons.types import Severity
import pytest

from clients.files.files_client import FilesClient
from clients.files.files_schema import UploadFileRequestSchema, UploadFileResponseSchema
from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
)
from config import settings
from fixtures.files import FileFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.files import (
    assert_create_file_with_empty_field_response,
    assert_delete_file_with_incorrect_file_id_response,
    assert_file_is_accessible,
    assert_file_not_found_response,
    assert_get_file_with_incorrect_file_id_response,
    assert_upload_file_response,
    assert_get_file_response,
)
from tools.assertions.schema import validate_json_schema


@pytest.mark.files
@pytest.mark.regression
@allure.tag(AllureTag.FILES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.parent_suite(AllureEpic.LMS)
@allure.feature(AllureFeature.FILES)
@allure.suite(AllureFeature.FILES)
class TestFiles:

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Upload file")
    def test_upload_file(self, files_client: FilesClient):
        """
        Тест проверяет, что при загрузке файла на сервер,
        в ответе сервера возвращается информация о файле.

        Args:
            files_client (FilesClient): HTTP-клиент для взаимодействия с сервером.

        Raises:
            AssertionError: Если данные в ответе не совпадают с ожидаемыми.
        """

        request = UploadFileRequestSchema(
            upload_file=settings.TEST_DATA.IMAGE_JPEG_FILE
        )
        response = files_client.upload_file_api(request)
        response_data = UploadFileResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_upload_file_response(request=request, response=response_data)
        assert_file_is_accessible(files_client, response_data.file.id, HTTPStatus.OK)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Get file")
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

    @pytest.mark.parametrize("field_name", ["filename", "directory"])
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Upload file with missing request field")
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
        allure.dynamic.title(f"Upload file with missing request field: {field_name}")
        request = UploadFileRequestSchema(
            upload_file=settings.TEST_DATA.IMAGE_JPEG_FILE
        )
        setattr(request, field_name, "")
        response = files_client.upload_file_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_file_with_empty_field_response(response_data, field_name)
        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Delete file")
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

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Get file with incorrect file id")
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

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Delete file with invalid id")
    def test_delete_user_with_invalid_id(
        self,
        files_client: FilesClient,
    ):
        """
        Тест удаления пользователя с некорректным id.

        Args:
            private_users_client (PrivateUsersClient): Клиент для работы с закрытыми users эндпоинтами API.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.UNPROCESSABLE_ENTITY.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            ValidationError: Если данные ответа не соответствуют схеме.
        """

        response = files_client.delete_file_api(file_id="incorrect-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_delete_file_with_incorrect_file_id_response(actual=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())
