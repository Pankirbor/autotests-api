from typing import TypedDict

from httpx import Response

from clients.api_client import ApiClient
from clients.users.users_schema import UserResponseSchema, UpdateUserRequestSchema


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
