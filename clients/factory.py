from httpx import Client

from auth.provider import IAuthProvider, AuthClientProvider
from auth.strategies import AuthStrategy, BearerStrategy
from builders.http import HttpClientBuilder
from builders.generic import GenericClientBuilder
from clients import (
    AuthenticationClient,
    CoursesClient,
    ExercisesClient,
    FilesClient,
    PrivateUsersClient,
    PublicUsersClient,
)


class ClientFactory:

    def __init__(
        self,
        http_builder: HttpClientBuilder,
        auth_provider: IAuthProvider | None = None,
        auth_strategy: AuthStrategy | None = None,
    ):
        self._client_builder = http_builder
        self._auth_provider = auth_provider
        self._auth_strategy = auth_strategy

    def set_auth_strategy(self, auth_strategy: AuthStrategy) -> None:
        self._auth_strategy = auth_strategy

    def set_auth_provider(self, auth_provider: IAuthProvider) -> None:
        self._auth_provider = auth_provider

    def create_public_client(self) -> Client:
        self._client_builder.reset()
        return self._client_builder.build()

    def create_authentication_client(self) -> AuthenticationClient:
        return GenericClientBuilder(self._client_builder, AuthenticationClient).build()

    def _create_authorized_builder(self, credentials: dict) -> HttpClientBuilder:
        if not self._auth_provider:
            raise ValueError("Необходим провайдер аутентификации")

        if not self._auth_strategy:
            raise ValueError("Необходимо указать стратегию аутентификации")

        provider = self._auth_provider(self.create_authentication_client())
        try:
            auth_data = provider.authenticate(credentials)
            authorized_builder = self._client_builder.copy().set_auth_header(
                self._auth_strategy(auth_data)
            )

            return authorized_builder

        except Exception as e:
            if isinstance(e, ValueError):
                raise ValueError(
                    "Ошибка аутентификации: некорректные учетные данные или токен"
                ) from e
            else:
                raise

    def create_public_users_client(self) -> PublicUsersClient:
        return GenericClientBuilder(self._client_builder, PublicUsersClient).build()

    def create_private_users_client(self, user: dict) -> PrivateUsersClient:
        authorized_builder = self._create_authorized_builder(user)
        return GenericClientBuilder(authorized_builder, PrivateUsersClient).build()

    def create_files_client(self, user: dict) -> FilesClient:
        authorized_builder = self._create_authorized_builder(user)
        return GenericClientBuilder(authorized_builder, FilesClient).build()

    def create_courses_client(self, user: dict) -> CoursesClient:
        authorized_builder = self._create_authorized_builder(user)
        return GenericClientBuilder(authorized_builder, CoursesClient).build()

    def create_exercises_client(self, user: dict) -> ExercisesClient:
        authorized_builder = self._create_authorized_builder(user)
        return GenericClientBuilder(authorized_builder, ExercisesClient).build()


client_factory = ClientFactory(
    http_builder=HttpClientBuilder(),
    auth_provider=AuthClientProvider,
    auth_strategy=BearerStrategy,
)
