import allure
from httpx import Response

from clients.api_client import ApiClient
from clients.authentication.authentication_schema import AuthenticationUserSchema
from clients.files.files_schema import UploadFileRequestSchema, UploadFileResponseSchema
from clients.private_http_builder import get_private_http_client


class FilesClient(ApiClient):
    """Клиент для взаимодействия с эндпоинтами API управления файлами."""

    @allure.step("Загружаем файл на сервер")
    def upload_file_api(self, request: UploadFileRequestSchema) -> Response:
        """Загружает файл на сервер.

        Args:
            request (FileUploadRequestDict): Данные для загрузки файла,
                включая путь к локальному файлу.

        Returns:
            Response: Ответ сервера после загрузки файла.
        """
        return self.post(
            "/api/v1/files",
            data=request.model_dump(
                by_alias=True,
                exclude={"upload_file"},
            ),
            files={"upload_file": open(request.upload_file, "rb")},
        )

    @allure.step("Получаем информацию о файле по file_id")
    def get_file_api(self, file_id: str) -> Response:
        """Получает информацию о файле по его идентификатору.

        Args:
            file_id (str): Уникальный идентификатор файла.

        Returns:
            Response: Ответ сервера с данными о запрошенном файле.
        """
        return self.get(f"/api/v1/files/{file_id}")

    @allure.step("Удаляем файл по file_id")
    def delete_file_api(self, file_id: str) -> Response:
        """Удаляет файл с сервера по его идентификатору.

        Args:
            file_id (str): Уникальный идентификатор файла.

        Returns:
            Response: Ответ сервера подтверждающий удаление файла.
        """
        return self.delete(f"/api/v1/files/{file_id}")

    def upload_file(self, request: UploadFileRequestSchema) -> UploadFileResponseSchema:
        """
        Загружает файл на сервер и возвращает информацию о нем.

        Args:
            request (UploadFileRequestSchema): Данные для загрузки файла.

        Returns:
            UploadFileResponseSchema: Сериализованный JSON-ответ сервера,
            содержащий информацию о загруженном файле.
        """
        response = self.upload_file_api(request)
        return UploadFileResponseSchema.model_validate_json(response.text)


def get_files_client(user: AuthenticationUserSchema) -> FilesClient:
    """
    Функция создаёт экземпляр FilesClient с уже настроенным HTTP-клиентом.

    Returns:
        FilesClient: Экземпляр FilesClient с настроенным HTTP-клиентом.
    """
    return FilesClient(client=get_private_http_client(user))
