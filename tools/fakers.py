from faker import Faker


class Fake:
    def __init__(self, faker: Faker):
        self.faker = faker

    def text(self) -> str:
        """
        Генерирует случайный текст

        Returns:
            str: Сгенерированный текст
        """
        return self.faker.text()

    def uuid4(self) -> str:
        """
        Генерирует случайный UUID4.

        Returns:
            str: Случайный UUID4.
        """
        return self.faker.uuid4()

    def email(self, domain: str | None = None) -> str:
        """
        Генерирует случайный email.

        Returns:
            str: Случайный email.
        """
        return self.faker.email(domain=domain)

    def sentence(self) -> str:
        """
        Генерирует случайное предложение.

        Returns:
            str: Случайное предложение.
        """
        return self.faker.sentence()

    def password(self) -> str:
        """
        Генерирует случайный пароль.

        Returns:
            str: Случайный пароль.
        """
        return self.faker.password()

    def last_name(self) -> str:
        """
        Генерирует случайную фамилию.

        Returns:
            str: Случайная фамилия.
        """
        return self.faker.last_name()

    def first_name(self) -> str:
        """
        Генерирует случайное имя.

        Returns:
            str: Случайное имя.
        """
        return self.faker.first_name()

    def middle_name(self) -> str:
        """
        Генерирует случайное отчество/среднее имя.

        Returns:
            str: Случайное отчество/среднее имя.
        """
        return self.faker.first_name()

    def estimated_time(self) -> str:
        """
        Генерирует строку с предполагаемым временем (например, "2 weeks").

        Returns:
            str: Строка с предполагаемым временем.
        """
        return f"{self.integer(1, 10)} weeks"

    def integer(self, start: int = 1, end: int = 100) -> int:
        """
        Генерирует случайное целое число в заданном диапазоне.

        Args:
          start (int): Начальное значение диапазона (по умолчанию 1).
          end (int): Конечное значение диапазона (по умолчанию 100).
        Returns:
          Случайное целое число.
        """
        return self.faker.random_int(start, end)

    def max_score(self) -> int:
        """
        Генерирует случайный максимальный балл в диапазоне от 50 до 100.

        Returns:
          Случайный балл.
        """
        return self.integer(50, 100)

    def min_score(self) -> int:
        """
        Генерирует случайный минимальный балл в диапазоне от 1 до 30.

        Returns:
          Случайный балл.
        """
        return self.integer(1, 30)


fake = Fake(faker=Faker("ru_RU"))
