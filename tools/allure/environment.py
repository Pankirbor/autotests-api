from pathlib import Path
import platform
import sys
from config import settings


def create_allure_environment():
    """
    Функция записывает в файл environment.properties
    """
    properties_data = list(settings.model_dump().items())
    properties_data.extend(
        [
            ("OS_INFO", f"{platform.system()} {platform.version()}"),
            ("PYTHON_VERSION", sys.version),
        ]
    )
    properties_content = "\n".join([f"{key}={value}" for key, value in properties_data])

    properties_path: Path = settings.ALLURE_RESULTS_DIR / "environment.properties"
    properties_path.write_text(properties_content, encoding="utf-8")
