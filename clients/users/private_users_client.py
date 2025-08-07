import allure
from httpx import Response

from clients.api_client import ApiClient
from clients.authentication.authentication_schema import AuthenticationUserSchema
from clients.users.users_schema import UserResponseSchema, UpdateUserRequestSchema
from clients.private_http_builder import get_private_http_client
from tools.routes.api_routes import APIRoutes


class PrivateUsersClient(ApiClient):
    """Клиент для работы с закрытыми эндпоинтами API управления пользователями.

    Предоставляет методы для получения, обновления и удаления информации о пользователях,
    требующих авторизации.
    """

    @allure.step("Получаем информацию о текущем пользователе")
    def get_user_me_api(self) -> Response:
        """Возвращает информацию о текущем авторизованном пользователе.

        Returns:
            Response: Ответ сервера с данными текущего пользователя.
        """
        return self.get(f"{APIRoutes.USERS.base_url}/me")

    @allure.step("Получаем информацию о пользователе по user_id")
    def get_user_api(self, user_id: str) -> Response:
        """Получает информацию о пользователе по его идентификатору.

        Args:
            user_id (str): Уникальный идентификатор пользователя.

        Returns:
            Response: Ответ сервера с данными запрошенного пользователя.
        """
        return self.get(APIRoutes.USERS.with_id(user_id))

    @allure.step("Обновляем информацию о пользователе по user_id")
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
            APIRoutes.USERS.with_id(user_id), json=request.model_dump(by_alias=True)
        )

    @allure.step("Удаляем пользователя по user_id")
    def delete_user_api(self, user_id: str) -> Response:
        """Удаляет пользователя по его идентификатору.

        Args:
            user_id (str): Уникальный идентификатор пользователя.

        Returns:
            Response: Ответ сервера подтверждающий удаление пользователя.
        """
        return self.delete(APIRoutes.USERS.with_id(user_id))

    def get_user(self, user_id: str) -> UserResponseSchema:
        """
        Метод получает информацию о пользователе по его идентификатору.

        Args:
            user_id (str): Уникальный идентификатор пользователя.

        Returns:
            UserResponseSchema: Объект с данными пользователя.
        """
        response = self.get_user_api(user_id)
        return UserResponseSchema.model_validate_json(response.text)


def get_private_users_client(user: AuthenticationUserSchema) -> PrivateUsersClient:
    """
    Функция создаёт экземпляр PrivateUsersClient с уже настроенным HTTP-клиентом.

    Args:
        user (AuthenticationUserSchema): Пользователь для авторизации.

    Returns:
        PrivateUsersClient: Экземпляр PrivateUsersClient с авторизованным HTTP-клиентом.
    """
    return PrivateUsersClient(client=get_private_http_client(user))
