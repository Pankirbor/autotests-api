from pydantic import BaseModel, ConfigDict, Field

from clients.files.files_schema import FileSchema
from clients.users.users_schema import UserSchema
from tools.fakers import fake


class BaseCourseSchema(BaseModel):
    """
    Базовая структура курса.
    """

    model_config = ConfigDict(populate_by_name=True)

    title: str
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class CourseSchema(BaseCourseSchema):
    """
    Описание структуры курса.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    preview_file: FileSchema = Field(alias="previewFile")
    created_by_user: UserSchema = Field(alias="createdByUser")


class GetCoursesQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка курсов.
    """

    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(alias="userId")


class CreateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на создание курса.
    """

    model_config = ConfigDict(populate_by_name=True)

    title: str = Field(default_factory=fake.sentence)
    min_score: int = Field(alias="minScore", default_factory=fake.min_score)
    max_score: int = Field(
        alias="maxScore",
        default_factory=fake.max_score,
    )
    description: str = Field(default_factory=fake.text)
    estimated_time: str = Field(
        alias="estimatedTime", default_factory=fake.estimated_time
    )
    preview_file_id: str = Field(alias="previewFileId", default_factory=fake.uuid4)
    created_by_user_id: str = Field(alias="createdByUserId", default_factory=fake.uuid4)


class UpdateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление курса.
    """

    title: str | None = Field(default_factory=fake.sentence)
    min_score: int | None = Field(alias="minScore", default_factory=fake.min_score)
    max_score: int | None = Field(alias="maxScore", default_factory=fake.max_score)
    description: str | None = Field(default_factory=fake.text)
    estimated_time: str | None = Field(
        alias="estimatedTime", default_factory=fake.estimated_time
    )


class CourseResponseSchema(BaseModel):
    """
    Описание структуры ответа создания курса.
    """

    course: CourseSchema


class GetCoursesResponseSchema(BaseModel):
    """
    Описание структуры ответа на запрос списка курсов.
    """

    courses: list[CourseSchema]
