from pydantic import BaseModel
import pytest

from clients.files.files_client import FilesClient, get_files_client
from clients.files.files_schema import UploadFileRequestSchema, UploadFileResponseSchema
from fixtures.users import UserFixture


class FileFixture(BaseModel):
    """
    Класс для хранения данных о загруженном файле.

    Attrs:
        request (UploadFileRequestSchema): Запрос для загрузки файла.
        response (UploadFileResponseSchema): Ответ сервера с информацией о загруженном файле.
    """

    request: UploadFileRequestSchema
    response: UploadFileResponseSchema

    @property
    def file_id(self) -> str:
        """
        Возвращает идентификатор загруженного файла.

        Returns:
            str: Идентификатор загруженного файла.
        """
        return self.response.file.id


@pytest.fixture
def files_client(function_user: UserFixture) -> FilesClient:
    """
    Фикстура возвращает экземпляр FilesClient с авторизованным HTTP-клиентом.

    Args:
        function_user (UserFixture): Объект с данными созданного пользователя.

    Returns:
        FilesClient: Экземпляр класса для работы с files эндпоинтами API.
    """
    return get_files_client(function_user.authentication_user)


@pytest.fixture
def function_file(files_client: FilesClient) -> FileFixture:
    """
    Фикстура загружает файл на сервер и возвращает информацию о нем.

    Args:
        files_client (FilesClient): Экземпляр класса для работы с files эндпоинтами API.

    Returns:
        FilesFixture: Объект с данными загруженного файла.
    """
    request = UploadFileRequestSchema(upload_file="./testdata/files/image.jpg")
    response = files_client.upload_file(request)
    return FileFixture(request=request, response=response)
