from typing import TypedDict

from httpx import Response

from clients.api_client import ApiClient
from clients.files.files_schema import UploadFileRequestSchema, UploadFileResponseSchema


class FilesClient(ApiClient):
    """Клиент для взаимодействия с эндпоинтами API управления файлами."""

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

    def get_file_api(self, file_id: str) -> Response:
        """Получает информацию о файле по его идентификатору.

        Args:
            file_id (str): Уникальный идентификатор файла.

        Returns:
            Response: Ответ сервера с данными о запрошенном файле.
        """
        return self.get(f"/api/v1/files/{file_id}")

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
