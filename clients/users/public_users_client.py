import allure
from httpx import Response

from clients.api_client import ApiClient
from clients.public_http_builder import get_public_http_client
from clients.users.users_schema import CreateUserRequestSchema, UserResponseSchema


class PublicUsersClient(ApiClient):
    """Клиент для работы с публичными эндпоинтами API управления пользователями."""

    @allure.step("Создаю пользователя")
    def create_user_api(self, request: CreateUserRequestSchema) -> Response:
        """Создает нового пользователя через API.

        Args:
            request (CreateUserRequestSchema): Данные для регистрации пользователя,
                включая email, пароль и персональные данные.

        Returns:
            Response: Ответ сервера после попытки создания пользователя.
        """
        return self.post("/api/v1/users", json=request.model_dump(by_alias=True))

    def create_user(self, request: CreateUserRequestSchema) -> UserResponseSchema:
        """Выполняет регистрацию пользователя и возвращает обработанный JSON-ответ.

        Args:
            request (CreateUserRequestSchema): Учетные данные и персональная информация
                нового пользователя (email, пароль, ФИО и т.д.).

        Returns:
            UserResponseSchema: Сериализованный JSON-ответ сервера, содержащий
                информацию о результате регистрации и, при успехе, токены доступа.
        """
        response = self.create_user_api(request)
        return UserResponseSchema.model_validate_json(response.text)


def get_public_users_client() -> PublicUsersClient:
    """
    Функция создаёт экземпляр PublicUsersClient с уже настроенным HTTP-клиентом.

    Returns:
        PublicUsersClient: Экземпляр класса для работы с публичными эндпоинтами API.
    """
    return PublicUsersClient(client=get_public_http_client())
