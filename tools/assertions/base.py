from typing import Any


def assert_status_code(actual: int, expected: int) -> None:
    """
    Проверяет статус код ответа.

    Args:
        actual (int): Ожидаемый статус код.
        expected (int): Текущий статус код.

    Raises:
        AssertionError: Если статус код не соответствует ожидаемому.
    """
    assert (
        actual == expected
    ), f"Incorrect response staus code. Expected: '{expected}', resived: '{actual}'"


def assert_equal(actual: Any, expected: Any, name: str) -> None:
    """
    Проверяет равенство двух значений.

    Args:
        actual (Any): Текущее значение.
        expected (Any): Ожидаемое значение.
        name (str): Название переменной для вывода в сообщении об ошибке.

    Raises:
        AssertionError: Если значения не равны.
    """
    assert (
        actual == expected
    ), f"Incorrect '{name}'. Expected: '{expected}', resived: '{actual}'"


def assert_is_true(actual: Any, name: str) -> None:
    """
    Проверяет, что значение является истинным.

    Args:
        actual (Any): Текущее значение.
        name (str): Название переменной для вывода в сообщении об ошибке.

    Raises:
        AssertionError: Если значение не является истинным.
    """
    assert actual, f"Incorrect value: '{name}'. Expected True, got: '{actual}'."
