from http import HTTPStatus

import allure
from allure_commons.types import Severity
import pytest

from clients.courses.constants import MAX_LENGTH_FIELDS
from clients.courses.courses_client import CoursesClient
from clients.courses.courses_schema import (
    GetCoursesQuerySchema,
    GetCoursesResponseSchema,
    UpdateCourseRequestSchema,
    CreateCourseRequestSchema,
    CourseResponseSchema,
)
from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
)
from fixtures.courses import CourseFixture, CoursesListFixture
from fixtures.users import UserFixture
from fixtures.files import FileFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.base import assert_status_code
from tools.assertions.courses import (
    assert_create_course_response,
    assert_create_course_with_empty_field_response,
    assert_create_course_with_incorrect_field_id_response,
    assert_create_or_update_course_with_too_long_title_response,
    assert_get_course_with_incorrect_id_response,
    assert_get_courses_response,
    assert_get_courses_with_incorrect_id_response,
    assert_get_courses_with_non_existent_id_response,
    assert_not_found_course_response,
    assert_update_course_response,
    assert_get_course_response,
)
from tools.assertions.schema import validate_json_schema
from tools.fakers import fake


@pytest.mark.regression
@pytest.mark.courses
@allure.tag(AllureTag.COURSES, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.parent_suite(AllureEpic.LMS)
@allure.feature(AllureFeature.COURSES)
@allure.suite(AllureFeature.COURSES)
class TestCourses:

    @allure.tag(AllureTag.GET_ENTITIES)
    @allure.story(AllureStory.GET_ENTITIES)
    @allure.sub_suite(AllureStory.GET_ENTITIES)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Get courses")
    def test_get_courses(
        self, function_courses_list: CoursesListFixture, courses_client: CoursesClient
    ):
        """
        Тест получения курсов.

        Args:
            function_courses_list (CoursesListFixture): Фикстура с данными списка курсов.
            courses_client (CoursesClient): Клиент для работы с курсами.
        """

        request = GetCoursesQuerySchema(user_id=function_courses_list.user_id)
        response = courses_client.get_courses_api(request)
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_courses_response(function_courses_list.response, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Create course")
    def test_create_course(
        self,
        courses_client: CoursesClient,
        function_user: UserFixture,
        function_file: FileFixture,
    ):
        """
        Тест создания курса.

        Args:
            courses_client (CoursesClient): Клиент для работы с курсами.
            function_user (UserFixture): Фикстура с данными пользователя.
            function_file (FileFixture): Фикстура с данными файла.
        """

        request = CreateCourseRequestSchema(
            preview_file_id=function_file.file_id,
            created_by_user_id=function_user.user_id,
        )
        response = courses_client.create_course_api(request)
        response_data = CourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_course_response(request=request, response=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Get course")
    def test_get_course(
        self, function_course: CourseFixture, courses_client: CoursesClient
    ):
        """
        Тест получения курса.

        Args:
            function_course (CourseFixture): Фикстура с данными курса.
            courses_client (CoursesClient): Клиент для работы с курсами.
        """
        response = courses_client.get_course_api(course_id=function_course.course_id)
        response_data = CourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_course_response(function_course.response, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Update course")
    def test_update_course(
        self, function_course: CourseFixture, courses_client: CoursesClient
    ):
        """
        Тест обновления курса.

        Args:
            function_course (CourseFixture): Фикстура с данными курса.
            courses_client (CoursesClient): Клиент для работы с курсами.
        """
        request = UpdateCourseRequestSchema()
        response = courses_client.update_course_api(
            course_id=function_course.course_id, request=request
        )
        response_data = CourseResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_course_response(request, response_data, function_course.course_id)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Delete course")
    def test_delete_course(
        self, function_course: CourseFixture, courses_client: CoursesClient
    ):
        """
        Тест удаления курса.

        Args:
            function_course (CourseFixture): Фикстура с данными курса.
            courses_client (CoursesClient): Клиент для работы с курсами.
        """

        delete_response = courses_client.delete_course_api(function_course.course_id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        get_response = courses_client.get_course_api(function_course.course_id)
        get_response_data = InternalErrorResponseSchema.model_validate_json(
            get_response.text
        )

        assert_status_code(get_response.status_code, HTTPStatus.NOT_FOUND)
        assert_not_found_course_response(get_response_data)

    @pytest.mark.parametrize(
        "field_name", ["title", "description", "preview_file_id", "created_by_user_id"]
    )
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Create course with empty required field")
    def test_create_course_with_empty_required_field(
        self, courses_client: CoursesClient, field_name: str
    ):
        """
        Тест создания курса с пустым обязательным полем.

        Args:
            courses_client (CoursesClient): Клиент для работы с курсами.
            field_name (str): Имя поля, которое будет пустым в запросе.
        """

        allure.dynamic.title(f"Attempt to create course with empty {field_name} field")
        request = CreateCourseRequestSchema()
        setattr(request, field_name, "")

        response = courses_client.create_course_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_course_with_empty_field_response(response_data, field_name)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize("field_name", ["preview_file_id", "created_by_user_id"])
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Create course with invalid id field")
    def test_create_course_with_invalid_id_field(
        self, courses_client: CoursesClient, field_name: str
    ):
        """
        Тест создания курса с некорректным идентификатором.

        Args:
            courses_client (CoursesClient): Клиент для работы с курсами.
            field_name (str): Имя поля, которое будет содержать
            некорректное значение в запросе.
        """

        allure.dynamic.title(
            f"Attempt to create course with invalid {field_name} field"
        )
        request = CreateCourseRequestSchema()
        setattr(request, field_name, "incorrect-id")
        response = courses_client.create_course_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_course_with_incorrect_field_id_response(response_data, field_name)

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Create course with too long title")
    def test_create_course_with_too_long_title(self, courses_client: CoursesClient):
        """
        Тест создания курса с слишком длинным названием.

        Args:
            courses_client (CoursesClient): Клиент для работы с курсами.
        """

        too_long_string = "a" * (MAX_LENGTH_FIELDS.get("title") + 1)
        request = CreateCourseRequestSchema(title=too_long_string)
        response = courses_client.create_course_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_or_update_course_with_too_long_title_response(
            response_data, too_long_string
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Update course with too long title")
    def test_update_course_with_too_long_title(
        self, courses_client: CoursesClient, function_course: CourseFixture
    ):
        """
        Тест обновления курса с слишком длинным названием.

        Args:
            courses_client (CoursesClient): Клиент для работы с курсами.
            function_course (CourseFixture): Фикстура с данными курса.
        """

        too_long_string = "a" * (MAX_LENGTH_FIELDS.get("title") + 1)
        request = UpdateCourseRequestSchema(title=too_long_string)
        response = courses_client.update_course_api(function_course.course_id, request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_or_update_course_with_too_long_title_response(
            response_data, too_long_string
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Get course with non-existent id")
    def test_get_course_with_non_existent_id(self, courses_client: CoursesClient):
        response = courses_client.get_course_api(course_id=fake.uuid4())
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_not_found_course_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Delete course with non-existent id")
    def test_delete_course_with_non_existent_id(self, courses_client: CoursesClient):
        response = courses_client.delete_course_api(course_id=fake.uuid4())
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_not_found_course_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Get courses with non-existent user_id")
    def test_get_courses_with_non_existent_id(self, courses_client: CoursesClient):
        request = GetCoursesQuerySchema(user_id=fake.uuid4())
        response = courses_client.get_courses_api(request)
        response_data = GetCoursesResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_courses_with_non_existent_id_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Get courses with incorrect user_id")
    def test_get_courses_with_incorrect_id(self, courses_client: CoursesClient):
        request = GetCoursesQuerySchema(user_id="incorrect-id")
        response = courses_client.get_courses_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_courses_with_incorrect_id_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Get course with incorrect user_id")
    def test_get_course_with_incorrect_id(self, courses_client: CoursesClient):
        response = courses_client.get_course_api(course_id="incorrect-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_course_with_incorrect_id_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())
