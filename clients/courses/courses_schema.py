from pydantic import BaseModel, ConfigDict, Field

from clients.files.files_schema import FileSchema
from clients.users.users_schema import UserSchema


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

    id: str
    preview_file: FileSchema = Field(alias="previewFile")
    created_by_user: UserSchema = Field(alias="createdByUser")


class GetCoursesQuerySchema(BaseModel):
    """
    Описание структуры запроса на получение списка курсов.
    """

    user_id: str = Field(alias="userId")


class CreateCourseRequestSchema(BaseCourseSchema):
    """
    Описание структуры запроса на создание курса.
    """

    preview_file_id: str = Field(alias="previewFileId")
    created_by_use_idr: str = Field(alias="createdByUserId")


class UpdateCourseRequestSchema(BaseModel):
    """
    Описание структуры запроса на обновление курса.
    """

    title: str | None
    max_score: int | None = Field(alias="maxScore")
    min_score: int | None = Field(alias="minScore")
    description: str | None
    estimated_time: str | None = Field(alias="estimatedTime")


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
