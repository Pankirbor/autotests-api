from enum import Enum


class APIRoutes(str, Enum):
    USERS = "/users"
    FILES = "/files"
    COURSES = "/courses"
    EXERCISES = "/exercises"
    AUTHENTICATION = "/authentication"

    def as_tag(self) -> str:
        return self[1:]

    def join_path(self, part: str, delimitr: str = "/"):
        base_url = "http://localhost:8001/api/v1"
        return f"{base_url}{self[:]}{delimitr}{part}"


if __name__ == "__main__":
    print(APIRoutes.USERS.as_tag())
    print(APIRoutes.USERS.join_path("me"))
    print(APIRoutes.USERS.join_path("1"))
    print(APIRoutes.USERS.join_path("?username=Leo", delimitr=""))
