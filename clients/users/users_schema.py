from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserSchema(BaseModel):
    """
    Описание структуры пользователя.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    email: EmailStr
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


class CreateUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание пользователя.
    """

    model_config = ConfigDict(populate_by_name=True)

    email: str
    password: str
    last_name: str = Field(alias="lastName")
    first_name: str = Field(alias="firstName")
    middle_name: str = Field(alias="middleName")


# Добавили описание структуры ответа создания пользователя
class UserResponseSchema(BaseModel):
    """
    Структура ответа с информацией о пользователе.
    """

    user: UserSchema


class GetUserResponseSchema(UserResponseSchema):
    """
    Описание структуры ответа получения пользователя.
    """

    pass


class UpdateUserRequestSchema(BaseModel):
    """Класс, определяющий структуру данных для обновления информации о пользователе.

    Содержит необязательные поля, которые могут быть изменены при редактировании профиля.
    Все поля допускают значение None, что означает отсутствие изменения конкретного параметра.
    """

    model_config = ConfigDict(populate_by_name=True)

    email: str | None
    last_name: str | None = Field(alias="lastName")
    first_name: str | None = Field(alias="firstName")
    middle_name: str | None = Field(alias="middleName")
