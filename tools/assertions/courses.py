from clients.courses.courses_schema import (
    CourseSchema,
    UpdateCourseRequestSchema,
    CourseResponseSchema,
    CreateCourseRequestSchema,
    GetCoursesResponseSchema,
)
from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
    ValidationErrorSchema,
)
from tools.assertions.base import assert_equal
from tools.assertions.errors import (
    assert_internal_error_response,
    assert_validation_error_response,
)
from tools.assertions.files import assert_file
from tools.assertions.users import assert_user


def assert_course(actual: CourseSchema, expected: CourseSchema):
    """
    Проверка соответствия данных курса.

    Args:
        actual (CourseSchema): Текущие данные курса.
        expected (CourseSchema): Ожидаемые данные курса.

    Raises:
        AssertionError: Если данные не совпадают.
    """
    assert_equal(actual.id, expected.id, "id")
    assert_equal(actual.title, expected.title, "title")
    assert_equal(actual.description, expected.description, "description")
    assert_equal(actual.estimated_time, expected.estimated_time, "estimated_time")
    assert_equal(actual.max_score, expected.max_score, "max_score")
    assert_equal(actual.min_score, expected.min_score, "min_score")
    assert_file(actual.preview_file, expected.preview_file)
    assert_user(actual.created_by_user, expected.created_by_user)


def assert_create_course_response(
    request: CreateCourseRequestSchema, response: CourseResponseSchema
):
    """
    Проверяет, что данные курса после создания соответствуют ожидаемым.

    Args:
        request (CreateCourseRequestSchema): Отправленные данные для создания курса.
        response (CourseResponseSchema): Ответ сервера после создания курса.

    Raises:
        AssertionError: Если данные не совпадают.
    """

    assert_equal(response.course.title, request.title, "title")
    assert_equal(response.course.description, request.description, "description")
    assert_equal(response.course.max_score, request.max_score, "max_score")
    assert_equal(response.course.min_score, request.min_score, "min_score")
    assert_equal(
        response.course.estimated_time,
        request.estimated_time,
        "estimated_time",
    )
    assert_equal(
        response.course.preview_file.id,
        request.preview_file_id,
        "preview_file_id",
    )
    assert_equal(
        response.course.created_by_user.id,
        request.created_by_user_id,
        "created_by_user_id",
    )


def assert_get_course_response(
    expected_response: CourseResponseSchema, response: CourseResponseSchema
):
    """
    Проверяет, что данные курса соответствуют ожидаемым.

    Args:
        expected_response (CourseResponseSchema): Ожидаемые данные курса.
        response (CourseResponseSchema): Ответ сервера после запроса курса.

    Raises:
        AssertionError: Если данные не совпадают.
    """
    assert_course(expected_response.course, response.course)


def assert_get_courses_response(
    expected_response: GetCoursesResponseSchema,
    response: GetCoursesResponseSchema,
):
    """
    Проверяет, что данные курсов соответствуют ожидаемым.

    Args:
        expected_response (GetCoursesResponseSchema): Ожидаемые данные курсов.
        response (GetCoursesResponseSchema): Ответ сервера после запроса курсов.
    Raises:
        AssertionError: Если данные не совпадают.
    """
    for index, course in enumerate(expected_response.courses):
        print("COURSE", course)
        assert_course(response.courses[index], course)


def assert_update_course_response(
    request: UpdateCourseRequestSchema, response: CourseResponseSchema, course_id: str
):
    """
    Проверяет, что данные курса после обновления соответствуют ожидаемым.

    Args:
        request (UpdateCourseRequestSchema): Отправленные данные для обновления курса.
        response (CourseResponseSchema): Ответ сервера после обновления курса.
        course_id (str): Идентификатор курса, который должен быть в ответе.

    Raises:
        AssertionError: Если данные не совпадают.
    """
    assert_equal(response.course.id, course_id, "id")

    for field_name in request.model_dump().keys():
        assert_equal(
            getattr(response.course, field_name),
            getattr(request, field_name),
            field_name,
        )


def assert_not_found_course_response(actual: InternalErrorResponseSchema):
    """
    Проверяет, что при запросе несуществующего курса сервер возвращает ошибку.

    Args:
        actual (InternalErrorResponseSchema): Ответ сервера после запроса курса.
    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    expected = InternalErrorResponseSchema(details="Course not found")
    assert_internal_error_response(actual, expected)


def assert_create_course_with_empty_field_response(
    actual: ValidationErrorResponseSchema, field_name: str
):
    """
    Проверяет, что при отправке пустого значения в обязательном поле,
    сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса курса.
        field_name (str): Имя поля, в котором должен быть пустой строковый параметр.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    expected = None
    if field_name in ["title", "description"]:
        expected = ValidationErrorResponseSchema(
            details=[
                ValidationErrorSchema(
                    type="string_too_short",
                    input="",
                    context={"min_length": 1},
                    message="String should have at least 1 character",
                    location=["body", field_name],
                )
            ]
        )
    elif field_name in ["preview_file_id", "created_by_user_id"]:
        camel_case_field_names = {
            "preview_file_id": "previewFileId",
            "created_by_user_id": "createdByUserId",
        }
        context_msg = "invalid length: expected length 32 for simple format, found 0"
        msg = f"Input should be a valid UUID, {context_msg}"
        expected = ValidationErrorResponseSchema(
            details=[
                ValidationErrorSchema(
                    type="uuid_parsing",
                    input="",
                    context={"error": context_msg},
                    message=msg,
                    location=["body", camel_case_field_names.get(field_name)],
                )
            ]
        )
    assert_validation_error_response(actual, expected)


def assert_create_course_with_incorrect_field_id_response(
    actual: ValidationErrorResponseSchema, field_name: str
):
    """
    Проверяет, что при отправке некорректного значения в поле с идентификатором,
    сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса курса.
        field_name (str): Имя поля, в котором должен быть некорректный идентификатор.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    camel_case_field_names = {
        "preview_file_id": "previewFileId",
        "created_by_user_id": "createdByUserId",
    }
    context_error_val = (
        f"invalid character: expected an optional prefix of "
        f"`urn:uuid:` followed by [0-9a-fA-F-], found `i` at 1"
    )
    msg = f"Input should be a valid UUID, {context_error_val}"
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="uuid_parsing",
                input="incorrect-id",
                context={"error": context_error_val},
                message=msg,
                loc=["body", camel_case_field_names.get(field_name)],
            )
        ]
    )
    assert_validation_error_response(actual, expected)


def assert_create_course_with_too_long_title_response(
    actual: ValidationErrorResponseSchema,
):
    """
    Проверяет, что при отправке слишком длинного значения в поле title,
    при создании курса сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_long",
                input="a" * 256,
                context={"max_length": 250},
                message="String should have at most 250 characters",
                location=["body", "title"],
            )
        ]
    )
    assert_validation_error_response(actual, expected)


def assert_update_course_with_too_long_title_response(
    actual: ValidationErrorResponseSchema,
):
    """
    Проверяет, что при отправке слишком длинного значения в поле title,
    при обновлении курса, сервер возвращает ошибку.

    Args:
        actual (ValidationErrorResponseSchema): Ответ сервера после запроса.

    Raises:
        AssertionError: Если данные в ответе не совпадают с ожидаемыми.
    """
    expected = ValidationErrorResponseSchema(
        details=[
            ValidationErrorSchema(
                type="string_too_long",
                input="a" * 256,
                context={"max_length": 250},
                message="String should have at most 250 characters",
                location=["body", "title"],
            )
        ]
    )
    assert_validation_error_response(actual, expected)
