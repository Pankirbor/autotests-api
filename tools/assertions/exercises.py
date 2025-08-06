import allure

from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
)
from clients.exercises.exercises_schema import (
    ExerciseSchema,
    ExerciseResponseSchema,
    CreateExerciseRequestSchema,
    GetExercisesResponseSchema,
    UpdateExerciseRequestSchema,
    GetExercisesQuerySchema,
)
from clients.exercises.constants import FIELD_NAME_MAPPING, MAX_LENGTH_FIELDS
from fixtures.exercises import ExercisesListFixture
from tools.assertions.base import assert_equal, assert_length
from tools.assertions.api_error_constants import ErrorContext
from tools.assertions.error_builder import ValidationErrorBuilder
from tools.assertions.errors import (
    assert_internal_error_response,
    assert_validation_error_response,
)


err_builder = ValidationErrorBuilder()


@allure.step("Проверяем соответсвие данных упражнения")
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


@allure.step("Проверяем ответ сервера на запрос создания упражнения")
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


@allure.step("Проверяем ответ сервера на запрос получения упражнения")
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


@allure.step("Проверяем ответ сервера на запрос обновления упражнения")
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


@allure.step("Проверяем ответ сервера на запрос несуществующего упражнения")
def assert_not_found_exercise_response(actual: InternalErrorResponseSchema):
    """
    Проверяет, что при запросе несуществующего упражнения сервер возвращает ошибку.

    Args:
        actual (InternalErrorResponseSchema): Ответ сервера после запроса упражнения.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """

    expected = InternalErrorResponseSchema(details="Exercise not found")

    assert_internal_error_response(actual=actual, expected=expected)


@allure.step("Проверяем ответ сервера на запрос списка упражнений")
def assert_get_exercises_response(
    request: GetExercisesQuerySchema,
    expected_response: ExercisesListFixture,
    response: GetExercisesResponseSchema,
):
    """
    Проверяет, что при запросе списка упражнений данные в ответе соответствуют ожиданиям.

    Args:
        request (GetExercisesQuerySchema): Отправленные данные для запроса списка упражнений.
        expected_response (ExercisesListFixture): Ожидаемый ответ.
        response (GetExercisesResponseSchema): Текущий ответ.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    assert_equal(expected_response.request.course_id, request.course_id, "course_id")
    assert_length(response.exercises, expected_response.response.exercises, "exercises")
    for index, exercise in enumerate(expected_response.response.exercises):
        assert_exercise(actual=response.exercises[index], expected=exercise)


@allure.step(
    "Проверяем ответ сервера на запрос создания упражнения с некорректным id курса"
)
def assert_create_exercise_with_invalid_course_id_response(
    actual: ValidationErrorResponseSchema,
):
    """
    Проверяет, что при отправке невалидного id курса в поле course_id,
    при создании упражнения сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса упражнения.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    expected = (
        err_builder.with_input("incorrect_course_id")
        .with_error(ErrorContext.INVALID_UUID_CHAR, char="i", position=1)
        .at_location("body", "courseId")
        .build()
    )
    assert_validation_error_response(actual=actual, expected=expected)


@allure.step(
    "Проверям ответ сервера после запроса на создание или обновление упражнения с пустым обязательным параметром"
)
def assert_create_or_update_exercise_with_empty_required_string_field_response(
    actual: ValidationErrorResponseSchema, field_name: str
):
    """
    Проверяет, что при отправке пустой строки в поле с обязательным строковым параметром,
    при создании или обновлении упражнения сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса упражнения.
        field_name (str): Имя поля, в котором должен быть пустой строковый параметр.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """

    if field_name == "course_id":
        err_params = {"err_context": ErrorContext.INVALID_UUID_LENGTH, "length": 0}
    else:
        err_params = {"err_context": ErrorContext.STRING_TOO_SHORT, "min_length": 1}

    expected = (
        err_builder.with_input("")
        .with_error(**err_params)
        .at_location("body", FIELD_NAME_MAPPING.get(field_name))
        .build()
    )

    assert_validation_error_response(actual=actual, expected=expected)


@allure.step(
    "Проверям ответ сервера после запроса на создание или обновление упражнения с слишком длинным строковым параметром"
)
def assert_create_or_update_exercise_with_too_long_string_field_response(
    actual: ValidationErrorResponseSchema, field_name: str, input_val: str
):
    """
    Проверяет, что при отправке слишком длинного значения в поле с строковым параметром,
    при создании или обновлении упражнения сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса упражнения.
        field_name (str): Имя поля, в котором должен быть слишком длинный строковый параметр.
        input_val (str): Значение, которое должно быть отправлено в поле.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """

    expected = (
        err_builder.with_input(input_val)
        .with_error(
            ErrorContext.STRING_TOO_LONG, max_length=MAX_LENGTH_FIELDS.get(field_name)
        )
        .at_location("body", FIELD_NAME_MAPPING.get(field_name))
        .build()
    )
    assert_validation_error_response(actual=actual, expected=expected)


@allure.step(
    "Проверям ответ сервера после запроса на создание или обновление упражнения с некорректным score"
)
def assert_create_or_update_exercise_with_incorrect_score_response(
    actual: ValidationErrorResponseSchema,
    request: UpdateExerciseRequestSchema,
):
    """
    Проверяет, что при отправке некорректного значения в поле minScore,
    при создании или обновлении упражнения сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса упражнения.
        request (UpdateExerciseRequestSchema): Отправленные данные для обновления.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """

    if request.min_score > request.max_score:
        expected = (
            err_builder.with_input(request.model_dump(by_alias=True))
            .with_error(ErrorContext.SCORE_VALIDATION)
            .at_location("body")
            .build()
        )
    else:
        expected = (
            err_builder.with_input(request.min_score)
            .with_error(ErrorContext.NON_NEGATIVE_NUMBER, ge=0)
            .at_location("body", "minScore")
            .build()
        )

    assert_validation_error_response(actual=actual, expected=expected)
