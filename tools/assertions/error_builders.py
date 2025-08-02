from typing import Any
from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
    ValidationErrorSchema,
)
from tools.assertions.api_error_constants import APIErrorConstants, APIErrorType


class ErrorBuilder:

    @staticmethod
    def string_to_short_error(
        field_name: str,
        input_value: str = "",
        min_length: int = 1,
        loc_prefix: str = "body",
    ) -> ValidationErrorSchema:
        return ValidationErrorSchema(
            type=APIErrorType.STRING_TOO_SHORT,
            input=input_value,
            context={"min_length": min_length},
            message=APIErrorConstants.Validation.get_string_too_short_msg(
                min_length=min_length
            ),
            location=[loc_prefix, field_name],
        )

    @staticmethod
    def uuid_parsing_error(
        input_value: str,
        location: list[str],
        error_type: str,
        **ctx_kwargs: Any,
    ) -> ValidationErrorSchema:
        """Создает ошибку парсинга UUID.

        Args:
            input_value: Некорректное входное значение
            location: Путь к параметру (например, ["path", "file_id"])
            error_type: Тип ошибки ("invalid_character" или "invalid_length")
            **ctx_kwargs: Параметры для контекста:
                - Для invalid_character: char, position
                - Для invalid_length: input_length
        """
        if error_type == "invalid_character":
            message = APIErrorConstants.UUID.get_message_invalid_uuid(
                ctx_kwargs["char"], ctx_kwargs["position"]
            )
            context = {
                "error": APIErrorConstants.UUID.ERROR_CHARACTER.format(
                    char=ctx_kwargs["char"], position=ctx_kwargs["position"]
                )
            }
        elif error_type == "invalid_length":
            message = APIErrorConstants.UUID.get_message_min_length(
                ctx_kwargs["input_length"]
            )
            context = {
                "error": APIErrorConstants.UUID.ERROR_MIN_LENGTH.format(
                    input_length=ctx_kwargs["input_length"]
                )
            }
        else:
            raise ValueError(f"Unknown UUID error type: {error_type}")

        return ValidationErrorSchema(
            type=APIErrorType.UUID,
            input=input_value,
            context=context,
            message=message,
            location=location,
        )

    @staticmethod
    def not_found_error(source: str) -> InternalErrorResponseSchema:
        if not hasattr(APIErrorConstants, source):
            raise ValueError(f"No error constants found for source: {source}")
        return InternalErrorResponseSchema(
            details=getattr(APIErrorConstants, source).NOT_FOUND,
        )

    @staticmethod
    def create_validation_response(
        *errors: ValidationErrorSchema,
    ) -> ValidationErrorResponseSchema:
        return ValidationErrorResponseSchema(details=list(errors))
