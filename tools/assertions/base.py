from typing import Any, Sized

import allure


@allure.step("Проверяем, что статус код ответа сервера соответствует {expected}")
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


@allure.step("Проверяем, что значение {name} соответствует ожидаемому {expected}")
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


@allure.step("Проверяем, что значение {name} является истинным")
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


def assert_length(actual: Sized, expected: Sized, name: str) -> None:
    """
    Проверяет соответствие длин коллекций.

    Args:
        actual (Sized): Текущая длина коллекции.
        expected (Sized): Ожидаемая длина коллекции.
        name (str): Название переменной для вывода в сообщении об ошибке.

    Raises:
        AssertionError: Если длины не совпадают.
    """
    with allure.step(f"Проверяем, что длина {name} соответствует ожидаемой {expected}"):
        assert len(actual) == len(
            expected
        ), f"Incorrect '{name}' length. Expected: '{len(expected)}', resived: '{len(actual)}'"
