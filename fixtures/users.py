from pydantic import BaseModel
import pytest

from clients.authentication.authentication_schema import AuthenticationUserSchema
from clients.users.users_schema import CreateUserRequestSchema, UserResponseSchema
from clients.users.public_users_client import PublicUsersClient, get_public_users_client
from clients.users.private_users_client import (
    PrivateUsersClient,
    get_private_users_client,
)


class UserFixture(BaseModel):
    """
    Класс для хранения данных созданного пользователя.

    Attrs:
        request (CreateUserRequestSchema): Запрос на создание пользователя.
        response (UserResponseSchema): Ответ сервера после создания пользователя.
    """

    request: CreateUserRequestSchema
    response: UserResponseSchema

    @property
    def email(self) -> str:
        """
        Объект-свойство email.

        Returns:
            str: Email пользователя.

        """
        return self.request.email

    @property
    def password(self) -> str:
        """
        Объект-свойство password.

        Returns:
            str: Пароль пользователя.
        """
        return self.request.password

    @property
    def authentication_user(self) -> AuthenticationUserSchema:
        """
        Объект-свойство authentication_user.

        Returns:
            AuthenticationUserSchema: Объект с данными для аутентификации.
        """
        return AuthenticationUserSchema(email=self.email, password=self.password)

    @property
    def user_id(self) -> str:
        """
        Объект-свойство user_id.

        Returns:
            str: ID пользователя.
        """
        return self.response.user.id


@pytest.fixture
def public_users_client() -> PublicUsersClient:
    """Фикстура возвращает экземпляр PublicUsersClient.

    Returns:
        PublicUsersClient: Экземпляр класса для работы
         с публичными users эндпоинтами API.
    """
    return get_public_users_client()


@pytest.fixture
def function_user(public_users_client: PublicUsersClient) -> UserFixture:
    """
    Фикстура создаёт пользователя и возвращает его данные.

    Args:
        public_users_client (PublicUsersClient): Клиент для работы с публичными эндпоинтами API.

    Returns:
        UserFixture: Объект с данными созданного пользователя.
    """
    request = CreateUserRequestSchema()
    response = public_users_client.create_user(request)

    return UserFixture(request=request, response=response)


@pytest.fixture
def function_second_user(public_users_client: PublicUsersClient) -> UserFixture:
    """
    Фикстура создаёт пользователя и возвращает его данные.

    Args:
        public_users_client (PublicUsersClient): Клиент для работы с публичными эндпоинтами API.

    Returns:
        UserFixture: Объект с данными созданного пользователя.
    """
    request = CreateUserRequestSchema()
    response = public_users_client.create_user(request)

    return UserFixture(request=request, response=response)


@pytest.fixture
def private_users_client(function_user) -> PrivateUsersClient:
    """
    Фикстура возвращает экземпляр PrivateUsersClient с авторизованным HTTP-клиентом.

    Args:
        function_user (UserFixture): Объект с данными созданного пользователя.

    Returns:
        PrivateUsersClient: Экземпляр класса для работы с закрытыми users эндпоинтами API.
    """
    return get_private_users_client(function_user.authentication_user)
