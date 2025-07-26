from typing import Protocol, TypeVar, Any

from httpx import Response
from pydantic import BaseModel, EmailStr

from clients.authentication.authentication_client import (
    AuthenticationClient,
    LoginRequestDict,
)

T = TypeVar("T", bound=Any)
Credentials = dict[str, Any]


class Token(BaseModel):
    tokenType: str
    accessToken: str
    refreshToken: str


class TokenResponse(BaseModel):
    token: Token


class UserCredentials(BaseModel):
    email: EmailStr
    password: str


class IAuthProvider(Protocol[T]):
    """Интерфейс для провайдеров аутентификации, определяющий базовые методы."""

    def authenticate(self, credintials: Credentials) -> T:
        """Выполняет аутентификацию пользователя.

        Args:
            credentials: Учетные данные в виде словаря

        Returns:
            Результат аутентификации (токен или другой тип)
        """
        pass

    def refresh(self, refresh_data: Credentials) -> T:
        """Обновляет данные доступа.

        Args:
            refresh_data (Credentials): Данные для обновления прав доступа.
        Returns:
            T: Новый данные доступа, полученные от провайдера аутентификации.
        """
        pass


class AuthClientProvider(IAuthProvider[Token]):
    """Провайдер аутентификации, реализующий логику работы с токенами через клиент API."""

    def __init__(self, auth_client: AuthenticationClient) -> None:
        """Инициализирует провайдер с клиентом аутентификации.

        Args:
            auth_client (AuthenticationClient): Объект клиента для взаимодействия
                с эндпоинтами аутентификации.
        """
        self._client = auth_client

    def _parse_token_response(self, response: Response) -> Token:
        """Парсит ответ сервера и извлекает токен доступа.

        Args:
            response (Response): Ответ от API после успешной аутентификации
                или обновления токена.

        Returns:
            Token: Объект токена доступа, извлеченный из JSON-ответа.
        """
        print(response.json())
        data = TokenResponse(**response.json())
        return data.token

    def authenticate(self, credintials: Credentials) -> Token:
        """Аутентифицирует пользователя по учетным данным и возвращает токен.

        Args:
            credintials (Credentials): Учетные данные пользователя (email, пароль и т.д.).

        Returns:
            Token: Токен доступа после успешной аутентификации.

        Raises:
            ValueError: Если входные данные некорректны или произошла ошибка аутентификации.
        """
        try:
            user_cred = UserCredentials(**credintials)
            print(f"{user_cred=}, {user_cred.model_dump()}")
            response = self._client.login_api(
                LoginRequestDict(**user_cred.model_dump())
            )
            return self._parse_token_response(response).accessToken
        except Exception as e:
            raise ValueError(f"Authentication failed: {str(e)}") from e

    def refresh(self, refresh_data: Credentials) -> Token:
        """Обновляет токен доступа с использованием refresh-токена.

        Args:
            refresh_data (Credentials): Refresh-токен, полученный при предыдущей аутентификации.

        Returns:
            Token: Новый токен доступа после обновления.

        Raises:
            ValueError: Если refresh_data не указан.
        """
        if not refresh_data.get("refreshToken"):
            raise ValueError("refreshToken обязателен для обновления токена")

        try:
            response = self._client.refresh_api(refresh_data)
            return self._parse_token_response(response).refreshToken
        except Exception as e:
            raise ValueError(
                f"Обновление токена завершилось с ошибкой: {str(e)}"
            ) from e
