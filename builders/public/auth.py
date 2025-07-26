from builders.http import HttpClientBuilder
from clients.authentication.authentication_client import AuthenticationClient


class AuthClientBuilder:
    """Строитель для создания клиентов аутентификации на основе HTTP-клиента."""

    def __init__(self, client_builder: HttpClientBuilder):
        """Инициализирует строитель с фабрикой HTTP-клиентов.

        Args:
            client_builder (HttpClientBuilder): Объект, отвечающий за создание
                базового HTTP-клиента для работы с API.
        """
        self._builder = client_builder

    def build(self) -> AuthenticationClient:
        """Создает и возвращает клиент аутентификации.

        Returns:
            AuthenticationClient: Готовый к использованию клиент для работы
                с эндпоинтами аутентификации.
        """
        http_client = self._builder.build()
        return AuthenticationClient(http_client)
