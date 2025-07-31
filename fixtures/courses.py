import pytest
from pydantic import BaseModel

from fixtures.users import UserFixture
from fixtures.files import FileFixture
from clients.courses.courses_client import CoursesClient, get_courses_client
from clients.courses.courses_schema import (
    CreateCourseRequestSchema,
    CourseResponseSchema,
)


class CourseFixture(BaseModel):
    """
    Класс для хранения данных курса.

    Attrs:
        request (CreateCourseRequestSchema): Данные для создания курса.
        response (CourseResponseSchema): Ответ сервера после создания курса.
    """

    request: CreateCourseRequestSchema
    response: CourseResponseSchema

    @property
    def course_id(self) -> str:
        """
        Получение идентификатора курса.

        Returns:
            str: Идентификатор курса.
        """
        return self.response.course.id


@pytest.fixture
def courses_client(function_user: UserFixture) -> CoursesClient:
    """
    Фикстура создает CoursesClient с уже настроенным HTTP-клиентом.

    Args:
        function_user (UserFixture): Фикстура с данными пользователя.

    Returns:
        CoursesClient: Экземпляр CoursesClient для работы с эндпоинтами courses.
    """
    return get_courses_client(function_user.authentication_user)


@pytest.fixture
def function_course(
    courses_client: CoursesClient,
    function_user: UserFixture,
    function_file: FileFixture,
) -> CourseFixture:
    """
    Фикстура создает курс.

    Args:
        courses_client (CoursesClient): Клиент для работы с курсами.
        function_user (UserFixture): Фикстура с данными пользователя.
        function_file (FileFixture): Фикстура с данными файла.

    Returns:
        CourseFixtures: Объект с данными курса.
    """
    request = CreateCourseRequestSchema(
        preview_file_id=function_file.file_id,
        created_by_user_id=function_user.user_id,
    )
    response = courses_client.create_course(request)

    return CourseFixture(request=request, response=response)
