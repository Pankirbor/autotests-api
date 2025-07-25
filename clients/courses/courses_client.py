from typing import TypedDict

from httpx import Response

from clients.api_client import ApiClient


class GetCoursesQueryDict(TypedDict):
    """
    Описание структуры запроса на получение списка курсов.
    """

    userId: str


class CreateCourseRequestDict(TypedDict):
    """
    Описание структуры запроса на создание курса.
    """

    title: str
    maxScore: int
    minScore: int
    description: str
    estimatedTime: str
    previewFileId: str
    createdByUserId: str


class UpdateCourseRequestDict(TypedDict):
    """
    Описание структуры запроса на обновление курса.
    """

    title: str | None
    maxScore: int | None
    minScore: int | None
    description: str | None
    estimatedTime: str | None


class CoursesClient(ApiClient):
    """Клиент для взаимодействия с эндпоинтами API управления курсами."""

    def get_courses_api(self, params: GetCoursesQueryDict) -> Response:
        """Получает список курсов с возможностью фильтрации и сортировки.

        Args:
            params (GetCoursesQueryDict): Параметры запроса для фильтрации.
                                          Словарь с userId.

        Returns:
            Response: Ответ сервера со списком курсов.
        """
        return self.get("/api/v1/courses", params=params)

    def get_course_api(self, course_id: str) -> Response:
        """Получает информацию о конкретном курсе по его идентификатору.

        Args:
            course_id (str): Уникальный идентификатор курса.

        Returns:
            Response: Ответ сервера с данными о запрошенном курсе.
        """
        return self.get(f"/api/v1/courses/{course_id}")

    def create_course_api(self, request: CreateCourseRequestDict) -> Response:
        """Создает новый курс на сервере.

        Args:
            request (CreateCourseRequestDict): Данные для создания курса.

        Returns:
            Response: Ответ сервера после создания курса.
        """
        return self.post(f"/api/v1/courses", json=request)

    def update_course_api(
        self, course_id: str, request: UpdateCourseRequestDict
    ) -> Response:
        """Обновляет информацию о курсе по его идентификатору.

        Args:
            course_id (str): Уникальный идентификатор курса.
            request (UpdateCourseRequestDict): Данные для обновления курса.
                Только указанные поля будут изменены.

        Returns:
            Response: Ответ сервера после обновления данных курса.
        """
        return self.patch(f"/api/v1/courses/{course_id}", json=request)

    def delete_course_api(self, course_id: str) -> Response:
        """Удаляет курс с сервера по его идентификатору.

        Args:
            course_id (str): Уникальный идентификатор курса.

        Returns:
            Response: Ответ сервера подтверждающий удаление курса.
        """
        return self.delete(f"/api/v1/courses/{course_id}")
