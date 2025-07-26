from httpx import Client

from builders.base import Builder


class HttpClientBuilder(Builder[Client]):
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self._config = {"base_url": "http://localhost:8001", "timeout": 10}

    def build(self) -> Client:
        return Client(**self._config)

    def set_base_url(self, url: str) -> "HttpClientBuilder":
        self._config["base_url"] = url
        return self

    def set_timeout(self, timeout: int) -> "HttpClientBuilder":
        if timeout > 0:
            self._config["timeout"] = timeout
            return self
