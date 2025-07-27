from typing import Any

from httpx import Client, Response, QueryParams, URL


class ApiClient:
    """Клиент для взаимодействия с внешним API через HTTP-запросы."""

    def __init__(self, client: Client):
        """Инициализирует объект ApiClient.

        Args:
            client (Client): Объект клиента, реализующий методы отправки HTTP-запросов.
        """
        self.client = client

    def get(self, url: URL | str, params: QueryParams | None = None) -> Response:
        """Отправляет HTTP GET-запрос на указанный URL.

        Args:
            url (URL | str): Адрес, по которому выполняется запрос.
            params (QueryParams | None, optional): Параметры запроса. Defaults to None.

        Returns:
            Response: Ответ сервера в виде объекта Response.
        """
        return self.client.get(url=url, params=params)

    def post(
        self,
        url: URL | str,
        json: Any | None = None,
        data: Any | None = None,
        files: Any | None = None,
    ) -> Response:
        """Отправляет HTTP POST-запрос на указанный URL.

        Args:
            url (URL | str): Адрес, по которому выполняется запрос.
            json: Any | None: Данные в формате JSON.
            data: RequestData | None: Форматированные данные формы (например, application/x-www-form-urlencoded).
            files: RequestFile | None: Файлы для загрузки на сервер.
        Returns:
            Response: Ответ сервера в виде объекта Response.
        """
        return self.client.post(url=url, json=json, data=data, files=files)

    def patch(self, url: URL | str, json: Any | None = None) -> Response:
        """Отправляет HTTP PATCH-запрос на указанный URL.

        Args:
            url (URL | str): Адрес, по которому выполняется запрос.
            json: Данные для обновления в формате JSON.

        Returns:
            Response: Ответ сервера в виде объекта Response.
        """
        return self.client.patch(url=url, json=json)

    def delete(self, url: URL | str) -> Response:
        """Отправляет HTTP DELETE-запрос на указанный URL.

        Args:
            url (URL | str): Адрес, по которому выполняется запрос.

        Returns:
            Response: Ответ сервера в виде объекта Response.
        """
        return self.client.delete(url=url)
