from functools import lru_cache

from httpx import Response

from clients.api_client import ApiClient
from clients.authentication.authentication_schema import AuthenticationUserSchema
from clients.users.users_schema import UserResponseSchema, UpdateUserRequestSchema
from clients.private_http_builder import get_private_http_client


class PrivateUsersClient(ApiClient):
    """Клиент для работы с закрытыми эндпоинтами API управления пользователями.

    Предоставляет методы для получения, обновления и удаления информации о пользователях,
    требующих авторизации.
    """

    def get_user_me_api(self) -> Response:
        """Возвращает информацию о текущем авторизованном пользователе.

        Returns:
            Response: Ответ сервера с данными текущего пользователя.
        """
        return self.get("/api/v1/users/me")

    def get_user_api(self, user_id: str) -> Response:
        """Получает информацию о пользователе по его идентификатору.

        Args:
            user_id (str): Уникальный идентификатор пользователя.

        Returns:
            Response: Ответ сервера с данными запрошенного пользователя.
        """
        return self.get(f"/api/v1/users/{user_id}")

    def update_user_api(
        self, user_id: str, request: UpdateUserRequestSchema
    ) -> Response:
        """Обновляет информацию о пользователе по его идентификатору.

        Args:
            user_id (str): Уникальный идентификатор пользователя.
            request (UserUpdateRequestDict): Данные для обновления профиля пользователя.

        Returns:
            Response: Ответ сервера после обновления данных пользователя.
        """
        return self.patch(
            f"/api/v1/users/{user_id}", json=request.model_dump(by_alias=True)
        )

    def delete_user_api(self, user_id: str) -> Response:
        """Удаляет пользователя по его идентификатору.

        Args:
            user_id (str): Уникальный идентификатор пользователя.

        Returns:
            Response: Ответ сервера подтверждающий удаление пользователя.
        """
        return self.delete(f"/api/v1/users/{user_id}")

    def get_user(self, user_id: str) -> UserResponseSchema:
        response = self.get_user_api(user_id)
        return UserResponseSchema.model_validate_json(response.text)


@lru_cache(maxsize=None)
def get_private_users_client(user: AuthenticationUserSchema) -> PrivateUsersClient:
    """
    Функция создаёт экземпляр PrivateUsersClient с уже настроенным HTTP-клиентом.

    Args:
        user (AuthenticationUserSchema): Пользователь для авторизации.

    Returns:
        PrivateUsersClient: Экземпляр PrivateUsersClient с авторизованным HTTP-клиентом.
    """
    return PrivateUsersClient(client=get_private_http_client(user))
