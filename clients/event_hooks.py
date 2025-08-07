import allure
from httpx import Request

from tools.http.curl import make_curl_request


def curl_event_hook(request: Request) -> None:
    """
    Записывает cURL команду в Allure.

    Args:
        request (Request): Запрос, который будет выполнен.
    """
    curl_command = make_curl_request(request=request)

    allure.attach(curl_command, "cURL command", allure.attachment_type.TEXT)
