from abc import ABC, abstractmethod
from typing import TypeVar, Generic


T = TypeVar("T")


class Builder(ABC, Generic[T]):

    @abstractmethod
    def build(self) -> T:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass
