from typing import Self
from pydantic import BaseModel, HttpUrl, FilePath, DirectoryPath
from pydantic_settings import BaseSettings, SettingsConfigDict

from tools.console_output_formatter import print_dict


class HTTPClientConfig(BaseModel):
    """
    Класс для хранения настроек HTTP-клиента.
    """

    URL: HttpUrl
    TIMEOUT: float

    @property
    def url_as_string(self):
        """
        Объекь-свойство, возвращающее URL в виде строки.
        """
        return f"{self.URL}"


class TestData(BaseModel):
    """
    Класс для хранения доступа к тестовым данным.
    """

    IMAGE_JPEG_FILE: FilePath

    @property
    def image_path_as_str(self) -> str:
        return str(self.IMAGE_JPEG_FILE)


class Settings(BaseSettings):
    """
    Класс для хранения настроек проекта.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter=".",
    )

    TEST_DATA: TestData
    HTTP_CLIENT: HTTPClientConfig
    APP_INTERHAL_HOST: HttpUrl
    ALLURE_RESULTS_DIR: DirectoryPath

    @classmethod
    def initialize(cls) -> Self:
        """
        Инициализирует настройки проекта.
        """
        allure_results_dir = DirectoryPath("./allure-results")
        allure_results_dir.mkdir(exist_ok=True)

        return Settings(ALLURE_RESULTS_DIR=allure_results_dir)


settings = Settings.initialize()
