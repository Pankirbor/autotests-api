from pprint import pprint


def print_dict(data: dict, title: str = "", message: str = "") -> None:
    """
    Красивый вывод словаря с заголовком и сообщением.

    Args:
        data: Словарь для вывода.
        title: Заголовок.
        message: Сообщение.
    """
    if title:
        print(f"\n\033[1m{title}\033[0m")  # Жирный текст
    if message:
        print(f"\033[36m{message}\033[0m")  # Голубой цвет

    pprint(data, indent=2, width=80, sort_dicts=False)
