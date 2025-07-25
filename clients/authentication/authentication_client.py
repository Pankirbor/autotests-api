from typing import TypedDict

from httpx import Response

from clients.api_client import ApiClient


class LoginRequestDict(TypedDict):
    """Класс, определяющий структуру данных для запроса входа в систему.

    Содержит обязательные поля для аутентификации пользователя.
    """

    username: str
    password: str


class RefreshRequestDict(TypedDict):
    """Класс, представляющий структуру данных для запроса обновления токена.

    Определяет обязательные ключи и их типы для передачи refresh-токена серверу.
    """

    refreshToken: str


class AuthenticationClient(ApiClient):
    """Клиент для взаимодействия с эндпоинтами аутентификации API."""

    def login_api(self, request: LoginRequestDict) -> Response:
        """Отправляет запрос на аутентификацию пользователя.

        Args:
            request (LoginRequestDict): Данные для входа в систему (логин/пароль и т.д.).

        Returns:
            Response: Ответ сервера после выполнения запроса на аутентификацию.
        """
        return self.post("/api/v1/authentication/login", json=request)

    def refresh_api(self, request: RefreshRequestDict) -> Response:
        """Обновляет токен доступа пользователя.

        Args:
            request (RefreshRequestDict): Данные для обновления токена (refresh token и т.д.).

        Returns:
            Response: Ответ сервера с новым токеном доступа.
        """
        return self.post("/api/v1/authentication/refresh", json=request)
