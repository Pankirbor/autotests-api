from typing import TypeVar, Generic, Type
from builders.http import HttpClientBuilder

T = TypeVar("T")


class GenericClientBuilder(Generic[T]):
    def __init__(self, client_builder: HttpClientBuilder, client_class: Type[T]):
        self._builder = client_builder
        self._client_class = client_class

    def build(self) -> T:
        return self._client_class(self._builder.build())
