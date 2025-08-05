from enum import Enum
from typing import Any


class ErrorContext(Enum):
    """Унифицированное хранилище шаблонов для всех типов ошибок."""

    STRING_TOO_SHORT = {
        "type": "string_too_short",
        "msg_template": "String should have at least {min_length} character",
        "context_template": {"min_length": "{min_length}"},
    }

    STRING_TOO_LONG = {
        "type": "string_too_long",
        "msg_template": "String should have at most {max_length} characters",
        "context_template": {"max_length": "{max_length}"},
    }

    NEGATIVE_NUMBER = {
        "type": "greater_than",
        "msg_template": "Input should be greater than {gt}",
        "context_template": {"gt": "{gt}"},
    }

    # UUID ошибки
    INVALID_UUID_CHAR = {
        "type": "uuid_parsing",
        "msg_template": "Input should be a valid UUID, {details}",
        "context_template": {
            "error": (
                "invalid character: expected an optional prefix of "
                "`urn:uuid:` followed by [0-9a-fA-F-], found `{char}` at {position}"
            )
        },
        "is_uuid": True,
    }

    INVALID_UUID_LENGTH = {
        "type": "uuid_parsing",
        "msg_template": "Input should be a valid UUID, {details}",
        "context_template": {
            "error": (
                "invalid length: expected length 32 for simple format, found {length}"
            )
        },
        "is_uuid": True,
    }

    SCORE_VALIDATION = {
        "type": "value_error",
        "msg_template": "Value error, max score should not be less than min score",
        "context_template": {"error": {}},
        "is_custom_error": True,  # Флаг для кастомных ошибок
    }

    NON_NEGATIVE_NUMBER = {
        "type": "greater_than_equal",
        "msg_template": "Input should be greater than or equal to {ge}",
        "context_template": {"ge": "{ge}"},
    }

    def format_error(self, **kwargs) -> tuple[str, dict[str, Any]]:
        """
        Форматирует сообщение и контекст с подставленными значениями.

        Args:
            **kwargs: Параметры для форматирования сообщения и контекста.

        Returns:
            tuple[str, dict[str, Any]]: Тип ошибки, контекст и сообщение.
        """
        formatted_ctx = {}
        for key, value in self.value["context_template"].items():
            if isinstance(value, str):
                value = value.format(**kwargs)
                formatted_ctx[key] = int(value) if value.isdigit() else value
            else:
                formatted_ctx[key] = value

        if self.value.get("is_uuid"):
            msg = self.value["msg_template"].format(details=formatted_ctx["error"])

        else:
            msg = self.value["msg_template"].format(**kwargs)

        return self.value["type"], formatted_ctx, msg
