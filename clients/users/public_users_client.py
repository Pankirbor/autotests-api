from typing import TypedDict

from httpx import Response

from clients.api_client import ApiClient


class User(TypedDict):
    """
    Описание структуры пользователя.
    """

    id: str
    email: str
    lastName: str
    firstName: str
    middleName: str


class CreateUserRequestDict(TypedDict):
    """
    Описание структуры запроса на создание пользователя.
    """

    email: str
    password: str
    lastName: str
    firstName: str
    middleName: str


# Добавили описание структуры ответа создания пользователя
class CreateUserResponseDict(TypedDict):
    """
    Описание структуры ответа создания пользователя.
    """

    user: User


class PublicUsersClient(ApiClient):
    """Клиент для работы с публичными эндпоинтами API управления пользователями."""

    def create_user_api(self, request: CreateUserRequestDict) -> Response:
        """Создает нового пользователя через API.

        Args:
            request (UserCreateRequestDict): Данные для регистрации пользователя,
                включая email, пароль и персональные данные.

        Returns:
            Response: Ответ сервера после попытки создания пользователя.
        """
        return self.post("/api/v1/users", json=request)

    def create_user(self, request: CreateUserRequestDict) -> CreateUserResponseDict:
        """Выполняет регистрацию пользователя и возвращает обработанный JSON-ответ.

        Args:
            request (CreateUserRequestDict): Учетные данные и персональная информация
                нового пользователя (email, пароль, ФИО и т.д.).

        Returns:
            CreateUserResponseDict: Сериализованный JSON-ответ сервера, содержащий
                информацию о результате регистрации и, при успехе, токены доступа.
        """
        response = self.create_user_api(request)
        return response.json()
