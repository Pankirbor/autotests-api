from httpx import Response

from clients.api_client import ApiClient

from clients.authentication.types import (
    LoginRequestDict,
    LoginResponseDict,
    RefreshRequestDict,
)


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

    def login(self, request: LoginRequestDict) -> LoginResponseDict:
        """Выполняет аутентификацию пользователя и возвращает обработанный JSON-ответ.

        Args:
            request (LoginRequestDict): Учетные данные для входа в систему
                (email и пароль пользователя).

        Returns:
            LoginResponseDict: Сериализованный JSON-ответ сервера, содержащий
                информацию о результате аутентификации и токенах.
        """
        response = self.login_api(request)
        return response.json()
