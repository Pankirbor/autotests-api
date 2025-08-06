import allure
from httpx import Response

from clients.api_client import ApiClient
from clients.public_http_builder import get_public_http_client

from clients.authentication.authentication_schema import (
    LoginRequestSchema,
    LoginResponseSchema,
    RefreshRequestSchema,
)


class AuthenticationClient(ApiClient):
    """Клиент для взаимодействия с эндпоинтами аутентификации API."""

    @allure.step("Авторизируюсь")
    def login_api(self, request: LoginRequestSchema) -> Response:
        """Отправляет запрос на аутентификацию пользователя.

        Args:
            request (LoginRequestSchema): Данные для входа в систему (логин/пароль и т.д.).

        Returns:
            Response: Ответ сервера после выполнения запроса на аутентификацию.
        """
        return self.post(
            "/api/v1/authentication/login", json=request.model_dump(by_alias=True)
        )

    @allure.step("Обновляю токен")
    def refresh_api(self, request: RefreshRequestSchema) -> Response:
        """Обновляет токен доступа пользователя.

        Args:
            request (RefreshRequestSchema): Данные для обновления токена (refresh token и т.д.).

        Returns:
            Response: Ответ сервера с новым токеном доступа.
        """
        return self.post(
            "/api/v1/authentication/refresh", json=request.model_dump(by_alias=True)
        )

    def login(self, request: LoginRequestSchema) -> LoginResponseSchema:
        """Выполняет аутентификацию пользователя и возвращает обработанный JSON-ответ.

        Args:
            request (LoginRequestSchema): Учетные данные для входа в систему
                (email и пароль пользователя).

        Returns:
            LoginResponseSchema: Сериализованный JSON-ответ сервера, содержащий
                информацию о результате аутентификации и токенах.
        """
        response = self.login_api(request)
        return LoginResponseSchema.model_validate_json(response.text)


def get_authentication_client() -> AuthenticationClient:
    """
    Функция создаёт экземпляр AuthenticationClient с уже настроенным HTTP-клиентом

    Returns:
        AuthenticationClient: Экземпляр AuthenticationClient с настроенным HTTP-клиентом.
    """
    return AuthenticationClient(client=get_public_http_client())
