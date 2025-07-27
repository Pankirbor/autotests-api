from typing import TypedDict

from httpx import Response

from clients.api_client import ApiClient


class CreateExerciseRequestDict(TypedDict):
    """Класс, определяющий структуру данных для создания нового упражнения.

    Содержит обязательные параметры, необходимые для инициализации упражнения в системе.
    """

    title: str
    courseId: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str


class UpdateExerciseRequestDict(TypedDict):
    """Класс, определяющий структуру данных для частичного обновления упражнения.

    Все поля являются необязательными и могут принимать значение None,
    что означает отсутствие изменения соответствующего параметра.
    """

    title: str | None
    maxScore: int | None
    minScore: int | None
    orderIndex: int | None
    description: str | None
    estimatedTime: str | None


class GetExercisesQueryDict(TypedDict):
    """Класс, определяющий структуру параметров запроса для получения списка упражнений.

    Используется для фильтрации упражнений по идентификатору курса.
    """

    courseId: str


class Exercise(TypedDict):
    """Класс, определяющий структуру данных упражнения.

    Содержит идентификатор, название, описание, оценки, порядковый номер,
    идентификатор курса и идентификатор пользователя, создавшего упражнение.
    """

    id: str
    title: str
    maxScore: int
    minScore: int
    orderIndex: int
    description: str
    estimatedTime: str


class GetExercisesResponseDict(TypedDict):
    """Класс, определяющий структуру ответа на запрос списка упражнений.

    Содержит список упражнений и общее количество найденных записей.
    """

    exercises: list[Exercise]


class ExerciseResponseDict(TypedDict):
    exercise: Exercise


class ExercisesClient(ApiClient):
    """Клиент для взаимодействия с эндпоинтами API управления упражнениями."""

    def get_exercises_api(self, params: GetExercisesQueryDict) -> Response:
        """Получает список упражнений с возможностью фильтрации.

        Args:
            params (GetExercisesQueryDict): Параметры запроса для фильтрации.

        Returns:
            Response: Ответ сервера со списком упражнений.
        """
        return self.get("/api/v1/exercises", params=params)

    def get_exercise_api(self, exercise_id: str) -> Response:
        """Получает информацию о конкретном упражнении по его идентификатору.

        Args:
            exercise_id (str): Уникальный идентификатор упражнения.

        Returns:
            Response: Ответ сервера с данными о запрошенном упражнении.
        """
        return self.get(f"/api/v1/exercises/{exercise_id}")

    def create_exercise_api(self, request: CreateExerciseRequestDict) -> Response:
        """Создает новое упражнение на сервере.

        Args:
            request (CreateExerciseRequestDict): Данные для создания упражнения,
                включая название, описание и другие параметры.

        Returns:
            Response: Ответ сервера после создания упражнения.
        """
        return self.post(f"/api/v1/exercises", json=request)

    def update_exercise_api(
        self, exercise_id: str, request: UpdateExerciseRequestDict
    ) -> Response:
        """Обновляет информацию об упражнении по его идентификатору.

        Args:
            exercise_id (str): Уникальный идентификатор упражнения.
            request (UpdateExerciseRequestDict): Данные для обновления упражнения.
                Только указанные поля будут изменены.

        Returns:
            Response: Ответ сервера после обновления данных упражнения.
        """
        return self.patch(f"/api/v1/exercises/{exercise_id}", json=request)

    def delete_exercise_api(self, exercise_id: str) -> Response:
        """Удаляет упражнение с сервера по его идентификатору.

        Args:
            exercise_id (str): Уникальный идентификатор упражнения.

        Returns:
            Response: Ответ сервера подтверждающий удаление упражнения.
        """
        return self.delete(f"/api/v1/exercises/{exercise_id}")

    def get_exercises(self, params: GetExercisesQueryDict) -> GetExercisesResponseDict:
        """Получает список упражнений с возможностью фильтрации.
        Args:
            params (GetExercisesQueryDict): Параметры запроса для фильтрации.
        Returns:
            GetExercisesResponseDict: Ответ сервера со списком упражнений.
        """
        response = self.get("/api/v1/exercises", params=params)
        return response.json()

    def create_exercise(
        self, request: CreateExerciseRequestDict
    ) -> ExerciseResponseDict:
        """
        Создает новое упражнение на сервере.
        Args:
            request (CreateExerciseRequestDict): Данные для создания упражнения,
                включая название, описание и другие параметры.
        Returns:
            ExerciseResponseDict: Ответ сервера после создания упражнения.
        """
        return self.create_exercise_api(request).json()

    def get_exercise(self, exercise_id: str) -> ExerciseResponseDict:
        """
        Получает информацию о конкретном упражнении по его идентификатору.
        Args:
            exercise_id (str): Уникальный идентификатор упражнения.
        Returns:
            ExerciseResponseDict: Ответ сервера с данными о запрошенном упражнении.
        """
        return self.get_exercise_api(exercise_id).json()

    def update_exercise(
        self, exercise_id: str, request: UpdateExerciseRequestDict
    ) -> ExerciseResponseDict:
        """
        Обновляет информацию об упражнении по его идентификатору.
        Args:
            exercise_id (str): Уникальный идентификатор упражнения.
            request (UpdateExerciseRequestDict): Данные для обновления упражнения.
                Только указанные поля будут изменены.
        Returns:
            ExerciseResponseDict: Ответ сервера после обновления данных упражнения.
        """
        return self.update_exercise_api(exercise_id, request).json()
