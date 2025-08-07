from enum import Enum
from config import settings


class APIRoutes(str, Enum):
    """Класс, представляющий маршруты API в виде строковых перечислений."""

    USERS = "/users"
    FILES = "/files"
    COURSES = "/courses"
    EXERCISES = "/exercises"
    AUTHENTICATION = "/authentication"

    @property
    def base_url(self) -> str:
        """
        Метод, возвращающий базовый URL для каждого маршрута API.
        Добавляет версию api указанную в settings.

        Returns:
            str: Базовый URL для каждого маршрута API.
        """
        return f"{settings.API_VERSION}{self.value}"

    def with_id(self, resource_id: str) -> str:
        """
        Метод, возвращающий URL для каждого маршрута API с указанием id ресурса.

        Args:
            resource_id (str): id ресурса.

        Returns:
            str: URL для каждого маршрута API с указанием id ресурса.
        """
        return f"{self.base_url}/{resource_id}"


if __name__ == "__main__":
    print(APIRoutes.USERS.base_url)
    print(f"{APIRoutes.USERS.base_url}/me")
    print(APIRoutes.USERS.with_id("1"))
