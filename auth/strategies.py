from abc import ABC, abstractmethod


class AuthStrategy(ABC):
    @abstractmethod
    def get_headers(self) -> dict[str, str]:
        pass


class BearerStrategy(AuthStrategy):
    def __init__(self, token: str):
        self.token = token

    def get_headers(self) -> dict[str, str]:
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
