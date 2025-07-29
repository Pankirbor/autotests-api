from httpx import Client

from clients.authentication.authentication_schema import (
    LoginRequestSchema,
    AuthenticationUserSchema,
)
from clients import (
    AuthenticationClient,
    CoursesClient,
    ExercisesClient,
    FilesClient,
    PublicUsersClient,
    PrivateUsersClient,
)


class ClientFactory:
    """Фабрика для создания клиентов взаимодействия с различными эндпоинтами API."""

    def __init__(self, base_url: str, timeout: int) -> None:
        """Инициализирует фабрику с базовым URL и таймаутом для HTTP-запросов.

        Args:
            base_url (str): Базовый URL API-сервера.
            timeout (int): Максимальное время ожидания ответа от сервера в секундах.
        """
        self.base_url = base_url
        self.timeout = timeout

    def _create_public_http_client(self) -> Client:
        """Создает публичный HTTP-клиент без аутентификации.

        Returns:
            Client: Объект HTTP-клиента для работы с публичными эндпоинтами.
        """
        return Client(base_url=self.base_url, timeout=self.timeout)

    def _create_private_http_client(self, user: AuthenticationUserSchema) -> Client:
        """Создает приватный HTTP-клиент с авторизацией через токен.

        Args:
            user (AuthenticationUserDict): Данные пользователя для входа
                (email и пароль).

        Returns:
            Client: Объект HTTP-клиента с заголовком Authorization для доступа
                к закрытым эндпоинтам.
        """
        authentication_client = self.create_authentication_client()
        login_response = authentication_client.login(
            LoginRequestSchema(email=user.email, password=user.password)
        )
        return Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={"Authorization": f"Bearer {login_response.token.access_token}"},
        )

    def create_authentication_client(self) -> AuthenticationClient:
        """Создает клиент для работы с эндпоинтами аутентификации.

        Returns:
            AuthenticationClient: Клиент для выполнения операций входа и обновления токена.
        """
        return AuthenticationClient(client=self._create_public_http_client())

    def create_public_users_client(self) -> PublicUsersClient:
        """Создает клиент для работы с публичными эндпоинтами управления пользователями.

        Returns:
            PublicUsersClient: Клиент для операций, не требующих авторизации.
        """
        return PublicUsersClient(client=self._create_public_http_client())

    def create_private_users_client(
        self, user: AuthenticationUserSchema
    ) -> PrivateUsersClient:
        """Создает клиент для работы с закрытыми эндпоинтами управления пользователями.

        Args:
            user (AuthenticationUserDict): Данные пользователя для получения
                авторизационного токена.

        Returns:
            PrivateUsersClient: Клиент для операций, требующих авторизации.
        """
        return PrivateUsersClient(client=self._create_private_http_client(user))

    def create_files_client(self, user: AuthenticationUserSchema) -> FilesClient:
        """Создает клиент для работы с файлами.

        Args:
            user (AuthenticationUserDict): Данные пользователя для получения
                авторизационного токена.

        Returns:
            FilesClient: Клиент для загрузки, получения и удаления файлов.
        """
        return FilesClient(client=self._create_private_http_client(user))

    def create_courses_client(self, user: AuthenticationUserSchema) -> CoursesClient:
        """Создает клиент для работы с курсами.

        Args:
            user (AuthenticationUserDict): Данные пользователя для получения
                авторизационного токена.

        Returns:
            CoursesClient: Клиент для управления курсами (создание, обновление и т.д.).
        """
        return CoursesClient(client=self._create_private_http_client(user))

    def create_exercises_client(
        self, user: AuthenticationUserSchema
    ) -> ExercisesClient:
        """Создает клиент для работы с упражнениями.

        Args:
            user (AuthenticationUserDict): Данные пользователя для получения
                авторизационного токена.

        Returns:
            ExercisesClient: Клиент для управления упражнениями (создание, обновление и т.д.).
        """
        return ExercisesClient(client=self._create_private_http_client(user))


client_factory = ClientFactory(base_url="http://localhost:8001", timeout=10)
