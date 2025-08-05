from typing import Any, Self

from clients.errors_schema import ValidationErrorResponseSchema, ValidationErrorSchema
from tools.assertions.api_error_constants import ErrorContext


class ValidationErrorBuilder:
    def __init__(self):
        """Инициализирует объект ValidationErrorBuilder."""

        self._reset()

    def _reset(self):
        """
        Обнуляет параметры ошибки.
        """
        self._type: str | None = None
        self._input: Any = None
        self._context: dict[str, Any] = {}
        self._message: str = ""
        self._location: list[str] = []

    def build(self):
        """
        Возвращает ошибку валидации. И обнуляет параметры.

        Returns:
            ValidationErrorResponseSchema: Ошибка валидации.
        """
        error = ValidationErrorResponseSchema(
            details=[
                ValidationErrorSchema(
                    type=self._type,
                    input=self._input,
                    context=self._context,
                    message=self._message,
                    location=self._location,
                )
            ]
        )
        self._reset()
        return error

    def with_input(self, value: str) -> Self:
        """
        Передает значение для проверки валидации.

        Args:
            value (str): Значение для проверки валидации.

        Returns:
            Self: Экземпляр класса с установленным значением для проверки валидации.
        """
        self._input = value
        return self

    def with_error(self, err_context: ErrorContext, **kwargs) -> Self:
        """
        Оперделяет тип ошибки, контекст и сообщение.

        Args:
            err_context (ErrorContext): Тип ошибки.(TOO_SHORT, TOO_LONG, NEGATIVE_NUMBER, INVALID_UUID_CHAR)
            **kwargs: Параметры для формирования контекста и сообщения.(max_length, min_length, gt, details)

        Returns:
            Self: Экземпляр класса с установленными типом ошибки, контекстом и сообщением.
        """
        self._type, self._context, self._message = err_context.format_error(**kwargs)
        return self

    def at_location(self, *location: str) -> Self:
        """
        Устанавливает локацию для ошибки.

        Args:
            *location (tuple[str, str]): Путь к ошибке в структуре данных.

        Returns:
            Self: Экземпляр класса с установленной локацией.
        """
        self._location = list(location)
        return self
