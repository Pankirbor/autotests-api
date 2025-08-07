import allure
from httpx import Response

from clients.api_client import ApiClient
from clients.authentication.authentication_schema import AuthenticationUserSchema
from clients.exercises.exercises_schema import (
    GetExercisesQuerySchema,
    GetExercisesResponseSchema,
    CreateExerciseRequestSchema,
    UpdateExerciseRequestSchema,
    ExerciseResponseSchema,
)
from clients.private_http_builder import get_private_http_client
from tools.routes.api_routes import APIRoutes


class ExercisesClient(ApiClient):
    """Клиент для взаимодействия с эндпоинтами API управления упражнениями."""

    @allure.step("Получаем список упражнений")
    def get_exercises_api(self, params: GetExercisesQuerySchema) -> Response:
        """Получает список упражнений с возможностью фильтрации.

        Args:
            params (GetExercisesQueryDict): Параметры запроса для фильтрации.

        Returns:
            Response: Ответ сервера со списком упражнений.
        """
        return self.get(
            APIRoutes.EXERCISES.base_url, params=params.model_dump(by_alias=True)
        )

    @allure.step("Получаем информацию об упражнении")
    def get_exercise_api(self, exercise_id: str) -> Response:
        """Получает информацию о конкретном упражнении по его идентификатору.

        Args:
            exercise_id (str): Уникальный идентификатор упражнения.

        Returns:
            Response: Ответ сервера с данными о запрошенном упражнении.
        """
        return self.get(APIRoutes.EXERCISES.with_id(exercise_id))

    @allure.step("Создаем упражнение")
    def create_exercise_api(self, request: CreateExerciseRequestSchema) -> Response:
        """Создает новое упражнение на сервере.

        Args:
            request (CreateExerciseRequestDict): Данные для создания упражнения,
                включая название, описание и другие параметры.

        Returns:
            Response: Ответ сервера после создания упражнения.
        """
        return self.post(
            APIRoutes.EXERCISES.base_url, json=request.model_dump(by_alias=True)
        )

    @allure.step("Обновляем упражнение")
    def update_exercise_api(
        self, exercise_id: str, request: UpdateExerciseRequestSchema
    ) -> Response:
        """Обновляет информацию об упражнении по его идентификатору.

        Args:
            exercise_id (str): Уникальный идентификатор упражнения.
            request (UpdateExerciseRequestDict): Данные для обновления упражнения.
                Только указанные поля будут изменены.

        Returns:
            Response: Ответ сервера после обновления данных упражнения.
        """
        return self.patch(
            APIRoutes.EXERCISES.with_id(exercise_id),
            json=request.model_dump(by_alias=True),
        )

    @allure.step("Удаляем упражнение")
    def delete_exercise_api(self, exercise_id: str) -> Response:
        """Удаляет упражнение с сервера по его идентификатору.

        Args:
            exercise_id (str): Уникальный идентификатор упражнения.

        Returns:
            Response: Ответ сервера подтверждающий удаление упражнения.
        """
        return self.delete(APIRoutes.EXERCISES.with_id(exercise_id))

    def get_exercises(
        self, params: GetExercisesQuerySchema
    ) -> GetExercisesResponseSchema:
        """Получает список упражнений с возможностью фильтрации.
        Args:
            params (GetExercisesQueryDict): Параметры запроса для фильтрации.
        Returns:
            GetExercisesResponseDict: Ответ сервера со списком упражнений.
        """
        response = self.get_exercises_api(params=params.model_dump(by_alias=True))
        return GetExercisesResponseSchema.model_validate_json(response.text)

    def create_exercise(
        self, request: CreateExerciseRequestSchema
    ) -> ExerciseResponseSchema:
        """
        Создает новое упражнение на сервере.
        Args:
            request (CreateExerciseRequestDict): Данные для создания упражнения,
                включая название, описание и другие параметры.
        Returns:
            ExerciseResponseDict: Ответ сервера после создания упражнения.
        """
        response = self.create_exercise_api(request)
        return ExerciseResponseSchema.model_validate_json(response.text)

    def get_exercise(self, exercise_id: str) -> ExerciseResponseSchema:
        """
        Получает информацию о конкретном упражнении по его идентификатору.
        Args:
            exercise_id (str): Уникальный идентификатор упражнения.
        Returns:
            ExerciseResponseDict: Ответ сервера с данными о запрошенном упражнении.
        """
        response = self.get_exercise_api(exercise_id)
        return ExerciseResponseSchema.model_validate_json(response.text)

    def update_exercise(
        self, exercise_id: str, request: UpdateExerciseRequestSchema
    ) -> ExerciseResponseSchema:
        """
        Обновляет информацию об упражнении по его идентификатору.
        Args:
            exercise_id (str): Уникальный идентификатор упражнения.
            request (UpdateExerciseRequestDict): Данные для обновления упражнения.
                Только указанные поля будут изменены.
        Returns:
            ExerciseResponseDict: Ответ сервера после обновления данных упражнения.
        """
        response = self.update_exercise_api(exercise_id, request)
        return ExerciseResponseSchema.model_validate_json(response.text)


def get_exercises_client(user: AuthenticationUserSchema) -> ExercisesClient:
    """
    Создает экземпляр ExercisesClient с уже настроенным HTTP-клиентом.

    Args:
        user (AuthenticationUserSchema): Данные пользователя для авторизации.

    Returns:
        ExercisesClient: Экземпляр ExercisesClient с настроенным HTTP-клиентом.
    """
    return ExercisesClient(client=get_private_http_client(user))
