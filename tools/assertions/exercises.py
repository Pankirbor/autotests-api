from clients.exercises.exercises_schema import (
    ExerciseSchema,
    ExerciseResponseSchema,
    CreateExerciseRequestSchema,
    GetExercisesResponseSchema,
    UpdateExerciseRequestSchema,
    GetExercisesQuerySchema,
)
from tools.assertions.base import assert_equal


def assert_exercise(actual: ExerciseSchema, expected: ExerciseSchema):
    """
    Проверка соответствия данных упражнения.

    Args:
        actual (ExerciseSchema): Текущие данные упражнения.
        expected (ExerciseSchema): Ожидаемые данные упражнения.

    Raises:
        AssertionError: Если данные не совпадают.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.course_id, expected.course_id, "course_id")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_equal(actual.order_index, expected.order_index, "order_index")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")


def assert_create_exercise_response(
    response: ExerciseResponseSchema,
    request: CreateExerciseRequestSchema,
):
    """
    Проверяет, что при создании упражнения данные в ответе соответствуют ожиданиям.

    Args:
        response (ExerciseResponseSchema): Ответ сервера после создания упражнения.
        request (CreateExerciseRequestSchema): Отправленные данные для создания.

    Raises:
        AssertionError: Если данные не совпадают.
    """
    for field_name in request.model_dump().keys():
        assert_equal(
            getattr(response.exercise, field_name),
            getattr(request, field_name),
            field_name,
        )


def assert_get_exercise_response(
    expected_response: ExerciseResponseSchema,
    response: ExerciseResponseSchema,
):
    """
    Проверка ответа на запрос получения упражнения.

    Args:
        expected_response (ExerciseResponseSchema): Ожидаемый ответ.
        response (ExerciseResponseSchema): Текущий ответ.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    assert_exercise(response.exercise, expected_response.exercise)


def assert_update_exercise_response(
    request: UpdateExerciseRequestSchema,
    response: ExerciseResponseSchema,
    exercise_id: int,
):
    """
    Проверяет, что при обновлении упражнения данные в ответе соответствуют ожиданиям.

    Args:
        request (UpdateExerciseRequestSchema): Отправленные данные для обновления.
        response (ExerciseResponseSchema): Ответ сервера после обновления.
        exercise_id (int): Идентификатор упражнения, который должен быть в ответе.

    Raises:
        AssertionError: Если данные не совпадают.
    """

    assert_equal(response.exercise.id, exercise_id, "id")

    for field_name in request.model_dump().keys():
        assert_equal(
            getattr(response.exercise, field_name),
            getattr(request, field_name),
            field_name,
        )
