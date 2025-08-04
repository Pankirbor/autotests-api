import pytest
from pydantic import BaseModel

from fixtures.users import UserFixture
from fixtures.courses import CourseFixture
from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    ExerciseResponseSchema,
)


class ExerciseFixture(BaseModel):
    """
    Класс с данными о созданном упражнении.

    Attrs:
        request (CreateExerciseRequestSchema):
            данные запроса на создание упражнения.

        response (ExerciseResponseSchema):
            данные ответа на запрос создания упражнения.
    """

    request: CreateExerciseRequestSchema
    response: ExerciseResponseSchema

    @property
    def exercise_id(self) -> str:
        """
        Получение идентификатора упражнения.

        Returns:
            str: идентификатор упражнения.
        """
        return self.response.exercise.id


@pytest.fixture
def exercises_client(function_user: UserFixture) -> ExercisesClient:
    """
    Фикстура для получения экземпляра класса ExercisesClient.

    Args:
        function_user (UserFixture): фикстура с данными пользователя.

    Returns:
        ExercisesClient:
        Экземпляр класса ExercisesClient для работы с эндпоинтами exercises.
    """
    return get_exercises_client(function_user.authentication_user)


@pytest.fixture
def function_exercise(
    exercises_client: ExercisesClient, function_course: CourseFixture
) -> ExerciseFixture:
    """
    Фикстура для создания упражнения.

    Args:
        function_course (CourseFixture): фикстура с данными курса.

    Returns:
        ExerciseFixture:
        Объект с данными о созданном упражнении.
    """
    request = CreateExerciseRequestSchema(course_id=function_course.course_id)
    response = exercises_client.create_exercise(request)

    return ExerciseFixture(request=request, response=response)
