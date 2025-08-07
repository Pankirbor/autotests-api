from httpx import Request, RequestNotRead


def make_curl_request(request: Request) -> str:
    """
    Функция преобразует httpx.Request в curl-запрос.

    Args:
        request (Request): Объект httpx.Request.

    Returns:
        str: curl-запрос для выполнения запроса.
    """
    items: list[str] = [f"curl -X '{request.method}'", f"'{request.url}'"]

    for header, value in request.headers.items():
        items.append(f"-H '{header}: {value}'")

    try:
        if body := request.content:
            items.append(f"-d '{body.decode('utf-8')}'")
    except RequestNotRead:
        pass

    return " \\\n ".join(items)
