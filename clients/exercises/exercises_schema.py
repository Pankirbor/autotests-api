from pydantic import BaseModel, ConfigDict, Field


class CreateExerciseRequestSchema(BaseModel):
    """Класс, определяющий структуру данных для создания нового упражнения.

    Содержит обязательные параметры, необходимые для инициализации упражнения в системе.
    """

    model_config = ConfigDict(populate_by_name=True)

    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class UpdateExerciseRequestSchema(BaseModel):
    """Класс, определяющий структуру данных для частичного обновления упражнения.

    Все поля являются необязательными и могут принимать значение None,
    что означает отсутствие изменения соответствующего параметра.
    """

    model_config = ConfigDict(populate_by_name=True)

    title: str | None
    course_id: str | None = Field(alias="courseId")
    max_score: int | None = Field(alias="maxScore")
    min_score: int | None = Field(alias="minScore")
    order_index: int | None = Field(alias="orderIndex")
    description: str | None
    estimated_time: str | None = Field(alias="estimatedTime")


class GetExercisesQuerySchema(BaseModel):
    """Класс, определяющий структуру параметров запроса для получения списка упражнений.

    Используется для фильтрации упражнений по идентификатору курса.
    """

    course_id: str = Field(alias="courseId")


class ExerciseSchema(BaseModel):
    """Класс, определяющий структуру данных упражнения.

    Содержит идентификатор, название, описание, оценки, порядковый номер,
    идентификатор курса и идентификатор пользователя, создавшего упражнение.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    course_id: str = Field(alias="courseId")
    max_score: int = Field(alias="maxScore")
    min_score: int = Field(alias="minScore")
    order_index: int = Field(alias="orderIndex")
    description: str
    estimated_time: str = Field(alias="estimatedTime")


class GetExercisesResponseSchema(BaseModel):
    """Класс, определяющий структуру ответа на запрос списка упражнений.

    Содержит список упражнений и общее количество найденных записей.
    """

    exercises: list[ExerciseSchema]


class ExerciseResponseSchema(BaseModel):
    exercise: ExerciseSchema
