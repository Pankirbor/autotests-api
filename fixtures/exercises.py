import pytest
from pydantic import BaseModel

from fixtures.users import UserFixture
from fixtures.courses import CourseFixture
from clients.exercises.exercises_client import ExercisesClient, get_exercises_client
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    ExerciseResponseSchema,
    GetExercisesQuerySchema,
    GetExercisesResponseSchema,
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


class ExercisesListFixture(BaseModel):
    """
    Класс для хранения списка упражнений.

    Attrs:
        request (GetExercisesQuerySchema):
            данные запроса на получение списка упражнений.

        response (GetExercisesResponseSchema):
            данные ответа на запрос получения списка упражнений.
    """

    request: GetExercisesQuerySchema
    response: GetExercisesResponseSchema


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


@pytest.fixture
def function_exercises(
    exercises_client: ExercisesClient, function_course: CourseFixture
) -> ExercisesListFixture:
    """
    Фикстура для получения списка упражнений.

    Args:
        exercises_client (ExercisesClient): экземпляр класса ExercisesClient.
        function_course (CourseFixture): фикстура с данными курса.

    Returns:
        ExercisesListFixture:
        Объект с данными о созданных упражнениях.
    """

    create_exercise_requests = [
        CreateExerciseRequestSchema(course_id=function_course.course_id)
        for _ in range(2)
    ]
    exercises = [
        exercises_client.create_exercise(request).exercise
        for request in create_exercise_requests
    ]
    return ExercisesListFixture(
        request=GetExercisesQuerySchema(
            course_id=function_course.course_id,
        ),
        response=GetExercisesResponseSchema(
            exercises=exercises,
        ),
    )
