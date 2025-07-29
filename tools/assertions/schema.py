from typing import Any

from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft202012Validator


def validate_json_schema(instance: Any, schema: Any) -> None:
    """
    Функция для валидации JSON-схемы.

    Args:
        instance (Any): Объект, который должен соответствовать схеме.
        schema (Any): Схема в формате JSON.

    Raises:
        ValidationError: Если объект не соответствует схеме.
    """
    try:
        validate(
            schema=schema,
            instance=instance,
            format_checker=Draft202012Validator.FORMAT_CHECKER,
        )
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")
