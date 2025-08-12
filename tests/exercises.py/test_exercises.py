from http import HTTPStatus

import allure
from allure_commons.types import Severity
import pytest

from clients.courses.constants import MAX_LENGTH_FIELDS
from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
)
from clients.exercises.exercises_client import ExercisesClient
from clients.exercises.exercises_schema import (
    CreateExerciseRequestSchema,
    ExerciseResponseSchema,
    GetExercisesQuerySchema,
    GetExercisesResponseSchema,
    UpdateExerciseRequestSchema,
)
from fixtures.courses import CourseFixture
from fixtures.exercises import ExerciseFixture, ExercisesListFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.exercises import (
    assert_create_exercise_response,
    assert_create_exercise_with_invalid_course_id_response,
    assert_create_or_update_exercise_with_empty_required_string_field_response,
    assert_create_or_update_exercise_with_incorrect_score_response,
    assert_create_or_update_exercise_with_too_long_string_field_response,
    assert_delete_exercise_with_incorrect_exercise_id_response,
    assert_get_exercise_response,
    assert_get_exercise_with_incorrect_exercise_id_response,
    assert_get_exercises_response,
    assert_get_exercises_with_incorrect_course_id_response,
    assert_get_exercises_with_non_existent_course_id_response,
    assert_not_found_exercise_response,
    assert_update_exercise_response,
)
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake


@pytest.mark.regression
@pytest.mark.exercises
@allure.tag(AllureTag.EXERCISES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.parent_suite(AllureEpic.LMS)
@allure.feature(AllureFeature.EXERCISES)
@allure.suite(AllureFeature.EXERCISES)
class TestExercises:

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Создание упражнения")
    def test_create_exercise(
        self, exercises_client: ExercisesClient, function_course: CourseFixture
    ):
        """
        Тест создания упражнения.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
            function_course (CourseFixture): Фикстура с данными курса.

        """

        request = CreateExerciseRequestSchema(course_id=function_course.course_id)
        response = exercises_client.create_exercise_api(request)
        response_data = ExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_exercise_response(response_data, request)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.title("Получение упражнения")
    def test_get_exercise(
        self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture
    ):
        """
        Тест получения информации об упражнении.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
            function_exercise (ExerciseFixture): Фикстура с данными упражнения.
        """

        response = exercises_client.get_exercise_api(function_exercise.exercise_id)
        response_data = ExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_exercise_response(response_data, function_exercise.response)

        validate_json_schema(response.json(), response_data.model_json_schema())

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.title("Обновление упражнения")
    def test_update_exercise(
        self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture
    ):
        """
        Тест обновления информации об упражнении.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
            function_exercise (ExerciseFixture): Фикстура с данными упражнения.
        """

        request = UpdateExerciseRequestSchema(
            course_id=function_exercise.response.exercise.course_id
        )
        response = exercises_client.update_exercise_api(
            request=request, exercise_id=function_exercise.exercise_id
        )
        response_data = ExerciseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_exercise_response(
            request=request,
            response=response_data,
            exercise_id=function_exercise.exercise_id,
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.title("Удаление упражнения")
    def test_delete_exercise(
        self, exercises_client: ExercisesClient, function_exercise: ExerciseFixture
    ):
        """
        Тест удаления упражнения.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
            function_exercise (ExerciseFixture): Фикстура с данными упражнения.
        """

        delete_response = exercises_client.delete_exercise_api(
            exercise_id=function_exercise.exercise_id
        )
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = exercises_client.get_exercise_api(
            exercise_id=function_exercise.exercise_id
        )
        get_response_data = InternalErrorResponseSchema.model_validate_json(
            get_response.text
        )

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_not_found_exercise_response(get_response_data)

        validate_json_schema(get_response.json(), get_response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.severity(Severity.BLOCKER)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.title("Получение списка упражнений")
    def test_get_exercises(
        self,
        exercises_client: ExercisesClient,
        function_course: CourseFixture,
        function_exercises: ExercisesListFixture,
    ):
        """
        Тест для проверки получения списка упражнений.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
            function_course (CourseFixture): Фикстура с данными курса.
            function_exercises (ExercisesListFixture): Фикстура с данными упражнений.
        """

        request = GetExercisesQuerySchema(course_id=function_course.course_id)
        response = exercises_client.get_exercises_api(request)
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)

        assert_get_exercises_response(
            request=request,
            expected_response=function_exercises,
            response=response_data,
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.title("Получение списка упражнений по некорректному course_id")
    def test_get_exercises_with_incorrect_course_id(
        self, exercises_client: ExercisesClient
    ):
        """
        Тест получения упражнений с некорректным course_id.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
        """
        request = GetExercisesQuerySchema(course_id="incorrect-id")
        response = exercises_client.get_exercises_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_exercises_with_incorrect_course_id_response(actual=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.title("Получение упражнений по несуществующему course_id")
    def test_get_exercises_with_non_existent_course_id(
        self, exercises_client: ExercisesClient
    ):
        """
        Тест получения упражнений с не существующим course_id.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
        """
        request = GetExercisesQuerySchema(course_id=fake.uuid4())
        response = exercises_client.get_exercises_api(request)
        response_data = GetExercisesResponseSchema.model_validate_json(response.text)
        assert_get_exercises_with_non_existent_course_id_response(actual=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.title("Получение упражнения по некорректному идентификатору")
    def test_create_exercise_with_invalid_course_id(
        self, exercises_client: ExercisesClient
    ):
        """
        Тест создания упражнения с некоррктным course_id.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
        """

        request = CreateExerciseRequestSchema(course_id="incorrect-id")
        response = exercises_client.create_exercise_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_exercise_with_invalid_course_id_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize(
        "field_name", ["title", "description", "course_id", "estimated_time"]
    )
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_exercise_with_empty_required_string_fields(
        self,
        exercises_client: ExercisesClient,
        field_name: str,
        function_course: CourseFixture,
    ):
        """
        Тест создания упражнения с пустым обязательным полем.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
            field_name (str): Имя поля, которое будет пустым в запросе.
            function_course (CourseFixture): Фикстура с данными курса.
        """
        allure.dynamic.title(
            f"Попытка создать упражнение с пустым обязательным полем {field_name}"
        )
        request = CreateExerciseRequestSchema(course_id=function_course.course_id)
        setattr(request, field_name, "")
        response = exercises_client.create_exercise_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_or_update_exercise_with_empty_required_string_field_response(
            response_data, field_name
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize("field_name", ["title", "estimated_time"])
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_exercise_with_too_long_string_fields(
        self,
        exercises_client: ExercisesClient,
        field_name: str,
        function_course: CourseFixture,
    ):
        """
        Тест создания упражнения с слишком длинным строковым полем.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
            field_name (str): Имя поля, которое будет содержать слишком длинное значение в запросе.
            function_course (CourseFixture): Фикстура с данными курса.
        """

        allure.dynamic.title(
            f"Создание упражнения с слишком длинным значением в {field_name} поле"
        )
        to_long_string = "a" * (MAX_LENGTH_FIELDS.get(field_name) + 1)
        request = CreateExerciseRequestSchema(course_id=function_course.course_id)
        setattr(request, field_name, to_long_string)
        response = exercises_client.create_exercise_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_or_update_exercise_with_too_long_string_field_response(
            response_data, field_name, to_long_string
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize("field_name", ["title", "description", "estimated_time"])
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_exercise_with_empty_required_string_fields(
        self,
        exercises_client: ExercisesClient,
        field_name: str,
        function_course: CourseFixture,
    ):
        """
        Тест обновления упражнения с пустым обязательным полем.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
            field_name (str): Имя поля, которое будет пустым в запросе.
            function_course (CourseFixture): Фикстура с данными курса.
        """

        allure.dynamic.title(
            f"Обновление упражнения с пустым обязательным полем {field_name}"
        )
        request = UpdateExerciseRequestSchema()
        setattr(request, field_name, "")
        response = exercises_client.update_exercise_api(
            function_course.course_id, request
        )
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_or_update_exercise_with_empty_required_string_field_response(
            response_data, field_name
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize("field_name", ["title", "estimated_time"])
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_exercise_with_too_long_string_fields(
        self,
        exercises_client: ExercisesClient,
        field_name: str,
        function_course: CourseFixture,
    ):
        """
        Тест обновления упражнения с слишком длинным строковым полем.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
            field_name (str): Имя поля, которое будет содержать слишком длинное значение в запросе.
            function_course (CourseFixture): Фикстура с данными курса.
        """

        allure.dynamic.title(
            f"Обновление упражнения со слишком длинным значением в поле {field_name}"
        )
        to_long_string = "a" * (MAX_LENGTH_FIELDS.get(field_name) + 1)
        request = UpdateExerciseRequestSchema()
        setattr(request, field_name, to_long_string)
        response = exercises_client.update_exercise_api(
            function_course.course_id, request
        )
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_or_update_exercise_with_too_long_string_field_response(
            response_data, field_name, to_long_string
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize(
        "min_score, max_score",
        [
            (100, 10),
            pytest.param(-10, 0, marks=pytest.mark.xfail(reason="В разработке")),
        ],
    )
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_create_exercise_with_incorrect_score(
        self,
        exercises_client: ExercisesClient,
        min_score: int,
        max_score: int,
        function_course: CourseFixture,
    ):
        """
        Тест создания упражнения с некорректными значениями min_score и max_score.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
            min_score (int): Минимальное значение для min_score.
            max_score (int): Максимальное значение для max_score.
            function_course (CourseFixture): Фикстура с данными курса.
        """
        allure.dynamic.title(
            f"Создание упражнения с некорректными значениями"
            f" {min_score=} - {max_score=}"
        )
        request = CreateExerciseRequestSchema(course_id=function_course.course_id)
        setattr(request, "min_score", min_score)
        setattr(request, "max_score", max_score)
        response = exercises_client.create_exercise_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_or_update_exercise_with_incorrect_score_response(
            response_data, request
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize(
        "min_score, max_score",
        [
            (100, 10),
            pytest.param(-10, 0, marks=pytest.mark.xfail(reason="В разработке")),
        ],
    )
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    def test_update_exercise_with_incorrect_score(
        self,
        exercises_client: ExercisesClient,
        min_score: int,
        max_score: int,
        function_course: CourseFixture,
    ):
        """
        Тест обновления упражнения с некорректными значениями min_score и max_score.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
            min_score (int): Минимальное значение для min_score.
            max_score (int): Максимальное значение для max_score.
            function_course (CourseFixture): Фикстура с данными курса.
        """
        allure.dynamic.title(
            f"Обновление упражнения с некорректными значениями"
            f" {min_score=} - {max_score=}"
        )

        request = UpdateExerciseRequestSchema()
        setattr(request, "min_score", min_score)
        setattr(request, "max_score", max_score)
        response = exercises_client.update_exercise_api(
            function_course.course_id, request
        )
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_or_update_exercise_with_incorrect_score_response(
            response_data, request
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Получение упражнения с некорректным exercise_id")
    def test_get_exercise_with_incorrect_exercise_id(
        self, exercises_client: ExercisesClient
    ):
        """
        Тест получения упражнения с некорректным id.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
        """
        response = exercises_client.get_exercise_api("incorrect-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_exercise_with_incorrect_exercise_id_response(actual=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Удаление упражнения с некорректным exercise_id")
    def test_delete_exercise_with_incorrect_exercise_id(
        self, exercises_client: ExercisesClient
    ):
        """
        Тест удаления упражнения с некорректным id.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
        """

        response = exercises_client.delete_exercise_api("incorrect-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_delete_exercise_with_incorrect_exercise_id_response(actual=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.xfail(reason="В разработке")
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Удаление упражнения с несуществующим exercise_id")
    def test_delete_exercise_with_non_existent_exercise_id(
        self, exercises_client: ExercisesClient
    ):
        """
        Тест удаления упражнения с несуществующим id.

        Args:
            exercises_client (ExercisesClient): Клиент для работы с упражнениями.
        """
        response = exercises_client.delete_exercise_api(exercise_id=fake.uuid4())
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_not_found_exercise_response(actual=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())
