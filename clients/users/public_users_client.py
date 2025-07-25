from typing import TypedDict

from httpx import Response

from clients.api_client import ApiClient


class UserCreateRequestDict(TypedDict):
    """Класс, определяющий структуру данных для создания нового пользователя.

    Содержит обязательные поля, необходимые для регистрации пользователя в системе.
    """

    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str


class PublicUsersClient(ApiClient):
    """Клиент для работы с публичными эндпоинтами API управления пользователями."""

    def create_user_api(self, request: UserCreateRequestDict) -> Response:
        """Создает нового пользователя через API.

        Args:
            request (UserCreateRequestDict): Данные для регистрации пользователя,
                включая email, пароль и персональные данные.

        Returns:
            Response: Ответ сервера после попытки создания пользователя.
        """
        return self.post("/api/v1/users", json=request)
