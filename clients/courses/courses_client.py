from httpx import Response

from clients.api_client import ApiClient
from clients.private_http_builder import get_private_http_client
from clients.authentication.authentication_schema import AuthenticationUserSchema
from clients.courses.courses_schema import (
    GetCoursesQuerySchema,
    CreateCourseRequestSchema,
    CourseResponseSchema,
    UpdateCourseRequestSchema,
)


class CoursesClient(ApiClient):
    """Клиент для взаимодействия с эндпоинтами API управления курсами."""

    def get_courses_api(self, params: GetCoursesQuerySchema) -> Response:
        """Получает список курсов с возможностью фильтрации и сортировки.

        Args:
            params (GetCoursesQuerySchema): Параметры запроса для фильтрации.

        Returns:
            Response: Ответ сервера со списком курсов.
        """
        return self.get("/api/v1/courses", params=params.model_dump(by_alias=True))

    def get_course_api(self, course_id: str) -> Response:
        """Получает информацию о конкретном курсе по его идентификатору.

        Args:
            course_id (str): Уникальный идентификатор курса.

        Returns:
            Response: Ответ сервера с данными о запрошенном курсе.
        """
        return self.get(f"/api/v1/courses/{course_id}")

    def create_course_api(self, request: CreateCourseRequestSchema) -> Response:
        """Создает новый курс на сервере.

        Args:
            request (CreateCourseRequestSchema): Данные для создания курса.

        Returns:
            Response: Ответ сервера после создания курса.
        """
        return self.post(f"/api/v1/courses", json=request.model_dump(by_alias=True))

    def update_course_api(
        self, course_id: str, request: UpdateCourseRequestSchema
    ) -> Response:
        """Обновляет информацию о курсе по его идентификатору.

        Args:
            course_id (str): Уникальный идентификатор курса.
            request (UpdateCourseRequestSchema): Данные для обновления курса.
                Только указанные поля будут изменены.

        Returns:
            Response: Ответ сервера после обновления данных курса.
        """
        return self.patch(
            f"/api/v1/courses/{course_id}", json=request.model_dump(by_alias=True)
        )

    def delete_course_api(self, course_id: str) -> Response:
        """Удаляет курс с сервера по его идентификатору.

        Args:
            course_id (str): Уникальный идентификатор курса.

        Returns:
            Response: Ответ сервера подтверждающий удаление курса.
        """
        return self.delete(f"/api/v1/courses/{course_id}")

    def create_course(self, request: CreateCourseRequestSchema) -> CourseResponseSchema:
        """
        Создает новый курс на сервере.

        Args:
            request (CreateCourseRequestSchema): Данные для создания курса.

        Returns:
            CourseResponseSchema: Ответ сервера после создания курса.

        """
        response = self.create_course_api(request)
        return CourseResponseSchema.model_validate_json(response.text)


def get_courses_client(user: AuthenticationUserSchema) -> CoursesClient:
    """
    Функция создаёт экземпляр CoursesClient с уже настроенным HTTP-клиентом.

    Returns:
        CoursesClient: Экземпляр CoursesClient с авторизованным HTTP-клиентом.
    """
    return CoursesClient(client=get_private_http_client(user))
