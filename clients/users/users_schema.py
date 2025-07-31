from pydantic import BaseModel, Field, ConfigDict, EmailStr

from tools.fakers import fake


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

    email: str = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    last_name: str = Field(alias="lastName", default_factory=fake.last_name)
    first_name: str = Field(alias="firstName", default_factory=fake.first_name)
    middle_name: str = Field(alias="middleName", default_factory=fake.middle_name)

    def get_login_data(self):
        """
        Метод для получения данных для входа в систему.

        Returns:
            dict: Словарь с данными для входа в систему.
        """
        return {
            "email": self.email,
            "password": self.password,
        }


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

    email: str | None = Field(default_factory=fake.email)
    last_name: str | None = Field(alias="lastName", default_factory=fake.last_name)
    first_name: str | None = Field(alias="firstName", default_factory=fake.first_name)
    middle_name: str | None = Field(
        alias="middleName", default_factory=fake.middle_name
    )
