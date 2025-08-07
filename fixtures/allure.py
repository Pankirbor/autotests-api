from typing import Iterator
import pytest

from tools.allure.environment import create_allure_environment


@pytest.fixture(scope="session", autouse=True)
def save_allure_environment_file() -> Iterator[None]:
    """
    Записывает переменные окруженя в allure-results после выполнения всех тестов.
    """
    yield
    create_allure_environment()
