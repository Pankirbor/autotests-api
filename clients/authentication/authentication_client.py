from httpx import Response

from clients.api_client import ApiClient

from clients.authentication.authentication_schema import (
    LoginRequestSchema,
    LoginResponseSchema,
    RefreshRequestSchema,
)


class AuthenticationClient(ApiClient):
    """Клиент для взаимодействия с эндпоинтами аутентификации API."""

    def login_api(self, request: LoginRequestSchema) -> Response:
        """Отправляет запрос на аутентификацию пользователя.

        Args:
            request (LoginRequestDict): Данные для входа в систему (логин/пароль и т.д.).

        Returns:
            Response: Ответ сервера после выполнения запроса на аутентификацию.
        """
        return self.post(
            "/api/v1/authentication/login", json=request.model_dump(by_alias=True)
        )

    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        """Обновляет токен доступа пользователя.

        Args:
            request (RefreshRequestDict): Данные для обновления токена (refresh token и т.д.).

        Returns:
            Response: Ответ сервера с новым токеном доступа.
        """
        return self.post(
            "/api/v1/authentication/refresh", json=request.model_dump(by_alias=True)
        )

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        """Выполняет аутентификацию пользователя и возвращает обработанный JSON-ответ.

        Args:
            request (LoginRequestDict): Учетные данные для входа в систему
                (email и пароль пользователя).

        Returns:
            LoginResponseDict: Сериализованный JSON-ответ сервера, содержащий
                информацию о результате аутентификации и токенах.
        """
        response = self.login_api(request)
        return LoginResponseSchema.model_validate_json(response.text)
