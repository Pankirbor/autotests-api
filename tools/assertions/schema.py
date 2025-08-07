from typing import Any

import allure
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft202012Validator

from tools.logger import get_logger

logger = get_logger("SCHEMA_ASSERTIONS")


@allure.step("Проверяем, соответствует ли ответ сервера JSON-схеме")
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
        logger.info("Проверяем, соответствует ли ответ сервера JSON-схеме")

        validate(
            schema=schema,
            instance=instance,
            format_checker=Draft202012Validator.FORMAT_CHECKER,
        )
    except ValidationError as e:
        print(f"Ошибка валидации: {e}")
