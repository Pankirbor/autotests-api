from pydantic import BaseModel, Field, EmailStr


class LoginRequestSchema(BaseModel):
    """Класс, определяющий структуру данных для запроса входа в систему.

    Содержит обязательные поля для аутентификации пользователя.

    Attrs:
        email (str): Email пользователя.
        password (str): Пароль пользователя.
    """

    email: str
    password: str


class AuthenticationUserSchema(LoginRequestSchema):
    """Схема данных для аутентификации пользователя.

    Наследует поля и валидацию из схемы LoginRequestSchema.
    Используется для проверки структуры данных при запросе аутентификации.

    Attrs:
        email (str): Email пользователя.
        password (str): Пароль пользователя.
    """

    pass


class RefreshRequestSchema(BaseModel):
    """Класс, представляющий структуру данных для запроса обновления токена.

    Определяет обязательные ключи и их типы для передачи refresh-токена серверу.

    Attrs:
        refresh_token (str): Refresh-токен для обновления доступа.
    """

    refresh_token: str = Field(alias="refreshToken")


class TokenSchema(BaseModel):
    """
    Описание структуры аутентификационных токенов.

    Attrs:
        token_type (str): Тип токена.
        access_token (str): Токен доступа.
        refresh_token (str): Токен обновления.
    """

    token_type: str = Field(alias="tokenType")
    access_token: str = Field(alias="accessToken")
    refresh_token: str = Field(alias="refreshToken")


class LoginResponseSchema(BaseModel):
    """
    Описание структуры ответа аутентификации.

    Attrs:
        token (TokenSchema): Объект токена.
    """

    token: TokenSchema
