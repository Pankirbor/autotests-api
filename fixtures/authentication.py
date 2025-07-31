import pytest

from clients.authentication.authentication_client import (
    AuthenticationClient,
    get_authentication_client,
)


@pytest.fixture
def authentication_client() -> AuthenticationClient:
    """Фикстура возвращает экземпляр AuthenticationClient.

    Returns:
        AuthenticationClient: Экземпляр класса для работы с аутентификацией.
    """
    return get_authentication_client()
