from enum import Enum


class APIRoutes(str, Enum):
    """Класс, представляющий маршруты API в виде строковых перечислений."""

    USERS = "/users"
    FILES = "/files"
    COURSES = "/courses"
    EXERCISES = "/exercises"
    AUTHENTICATION = "/authentication"

    def as_tag(self) -> str:
        """Возвращает имя маршрута без начального слэша для использования в тегах документации.

        Returns:
            str: Имя маршрута без первого символа (слэша).
        """
        return self[1:]

    def join_path(self, part: str, delimitr: str = "/") -> str:
        """Формирует полный URL для указанного маршрута и части пути.

        Args:
            part (str): Дополнительная часть пути для добавления.
            delimitr (str, optional): Разделитель между основным маршрутом и частью пути.
                                      По умолчанию используется "/".

        Returns:
            str: Полный URL в формате "http://localhost:8001/api/v1/{маршрут}/{часть_пути}".
        """
        base_url = "http://localhost:8001/api/v1"
        return f"{base_url}{self[:]}{delimitr}{part}"


if __name__ == "__main__":
    print(APIRoutes.USERS.as_tag())
    print(APIRoutes.USERS.join_path("me"))
    print(APIRoutes.USERS.join_path("1"))
    print(APIRoutes.USERS.join_path("?username=Leo", delimitr=""))
