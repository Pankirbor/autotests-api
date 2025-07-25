from typing import TypedDict

from httpx import Response

from clients.api_client import ApiClient


class UserUpdateRequestDict(TypedDict):
    """Класс, определяющий структуру данных для обновления информации о пользователе.

    Содержит необязательные поля, которые могут быть изменены при редактировании профиля.
    Все поля допускают значение None, что означает отсутствие изменения конкретного параметра.
    """

    email: str | None
    lastName: str | None
    firstName: str | None
    middleName: str | None


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

    def update_user_api(self, user_id: str, request: UserUpdateRequestDict) -> Response:
        """Обновляет информацию о пользователе по его идентификатору.

        Args:
            user_id (str): Уникальный идентификатор пользователя.
            request (UserUpdateRequestDict): Данные для обновления профиля пользователя.

        Returns:
            Response: Ответ сервера после обновления данных пользователя.
        """
        return self.patch(f"/api/v1/users/{user_id}", json=request)

    def delete_user_api(self, user_id: str) -> Response:
        """Удаляет пользователя по его идентификатору.

        Args:
            user_id (str): Уникальный идентификатор пользователя.

        Returns:
            Response: Ответ сервера подтверждающий удаление пользователя.
        """
        return self.delete(f"/api/v1/users/{user_id}")
