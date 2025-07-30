from uuid import uuid4

from pydantic import BaseModel, Field, EmailStr
from tools.fakers import fake
from tools.console_output_formatter import print_dict


class BaseUserSchema(BaseModel):
    """
    Базовая схема данных пользователя для сериализации/десериализации.

    Описывает структуру данных пользователя с использованием Pydantic-моделей.
    Содержит поля с алиасами для соответствия формату JSON API.

    Attrs:
        id (str): Уникальный идентификатор пользователя.
        email (EmailStr): Email пользователя с автоматически генерируемым значением по умолчанию.
        last_name (str): Фамилия пользователя (соответствует ключу 'lastName' в JSON).
        first_name (str): Имя пользователя (соответствует ключу 'firstName' в JSON).
        middle_name (str): Отчество пользователя (соответствует ключу 'middleName' в JSON).
    """

    email: EmailStr = Field(
        default_factory=fake.email,
        description="Электронная почта пользователя (валидный email)",
    )

    last_name: str = Field(alias="lastName", description="Фамилия пользователя")

    first_name: str = Field(alias="firstName", description="Имя пользователя")

    middle_name: str = Field(alias="middleName", description="Отчество пользователя")


class UserSchema(BaseUserSchema):
    """
    Модель данных пользователя с идентификатором.

    Расширяет базовую схему пользователя, добавляя уникальный идентификатор.
    Используется для представления полной информации о пользователе в системе.

    Attrs:
        id (str): Идентификатор пользователя в формате UUIDv4.

    Если значение не указано явно, генерируется случайный UUIDv4 при инициализации объекта.
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Уникальный идентификатор пользователя,генерируется автоматически при создании",
    )


class CreateUserRequestSchema(BaseUserSchema):
    """
    Схема данных для запроса создания пользователя.

    Наследует поля и валидацию из базовой схемы BaseUserSchema.
    Используется для проверки структуры и корректности данных перед
    отправкой запроса на создание пользователя.
    """

    password: str


class CreateUserResponseSchema(BaseModel):
    """
    Модель данных ответа при успешном создании пользователя.

    Описывает структуру JSON-ответа, возвращаемого сервером после
    успешной регистрации пользователя.
    Содержит информацию о созданном пользователе.
    """

    user: UserSchema


user_data = {"lastName": "Иванов", "firstName": "Иван", "middleName": "Иванович"}
user = UserSchema(**user_data)
user_request = CreateUserRequestSchema(**user.model_dump(exclude={"id"}, by_alias=True))
create_user_response = CreateUserResponseSchema(user=user)

if __name__ == "__main__":
    print_dict(
        user.model_dump(),
        title="Пользователь:",
        message="Созданный с дефолтными значениями:",
    )
    print_dict(
        user_request.model_dump(),
        title="Запрос на создание пользователя:",
        message="Сгенерированный на основе user:",
    )
    print_dict(
        create_user_response.model_dump(),
        title="Ответ на создание пользователя:",
        message="Сгенерированный на основе user:",
    )
