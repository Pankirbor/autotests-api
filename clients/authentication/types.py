from typing import TypedDict


class LoginRequestDict(TypedDict):
    """Класс, определяющий структуру данных для запроса входа в систему.

    Содержит обязательные поля для аутентификации пользователя.
    """

    email: str
    password: str


class RefreshRequestDict(TypedDict):
    """Класс, представляющий структуру данных для запроса обновления токена.

    Определяет обязательные ключи и их типы для передачи refresh-токена серверу.
    """

    refreshToken: str


class Token(TypedDict):  # Добавили структуру с токенами аутентификации
    """
    Описание структуры аутентификационных токенов.
    """

    tokenType: str
    accessToken: str
    refreshToken: str


class LoginResponseDict(TypedDict):
    """
    Описание структуры ответа аутентификации.
    """

    token: Token
