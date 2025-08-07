from functools import lru_cache

from httpx import Client

from clients.authentication.authentication_client import get_authentication_client
from clients.authentication.authentication_schema import (
    AuthenticationUserSchema,
    LoginRequestSchema,
)
from config import settings
from clients.event_hooks import (
    curl_event_hook,
    log_request_event_hook,
    log_response_event_hook,
)


@lru_cache(maxsize=None)
def get_private_http_client(user: AuthenticationUserSchema) -> Client:
    """
    Функция создаёт экземпляр httpx.Client с аутентификацией пользователя.

    Args:
        user (AuthenticationUserSchema): Данные пользователя для входа.

    Returns:
        Client: Объект httpx.Client с настроенным заголовком авторизации.
    """
    authentication_client = get_authentication_client()

    login_request = LoginRequestSchema(email=user.email, password=user.password)
    login_response = authentication_client.login(login_request)

    return Client(
        timeout=settings.HTTP_CLIENT.TIMEOUT,
        base_url=settings.HTTP_CLIENT.url_as_string,
        headers={"Authorization": f"Bearer {login_response.token.access_token}"},
        event_hooks={
            "request": [curl_event_hook, log_request_event_hook],
            "response": [log_response_event_hook],
        },
    )
