from typing import TypedDict

from httpx import Response

from clients.api_client import ApiClient


class FileUploadRequestDict(TypedDict):
    """Класс, определяющий структуру данных для запроса загрузки файла.

    Содержит обязательные параметры, необходимые для передачи файла на сервер.
    """

    filename: str
    directory: str
    upload_file: str


class FilesClient(ApiClient):
    """Клиент для взаимодействия с эндпоинтами API управления файлами."""

    def upload_file_api(self, request: FileUploadRequestDict) -> Response:
        """Загружает файл на сервер.

        Args:
            request (FileUploadRequestDict): Данные для загрузки файла,
                включая путь к локальному файлу.

        Returns:
            Response: Ответ сервера после загрузки файла.
        """
        return self.post(
            "/api/v1/files",
            data=request,
            files={"upload_file": open(request["upload_file"], "rb")},
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
