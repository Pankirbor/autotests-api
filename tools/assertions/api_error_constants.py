from enum import Enum


class APIErrorType(str, Enum):
    UUID = "uuid_parsing"
    STRING_TOO_SHORT = "string_too_short"
    STRING_TOO_LONG = "string_too_long"


class APIErrorConstants:
    """Класс для хранения констант ошибок API."""

    class UUID:
        INVALID = "Input should be a valid UUID,"
        ERROR_CHARACTER = (
            "invalid character: expected an optional prefix of `urn:uuid:` followed"
            " by [0-9a-fA-F-], found `{char}` at {position}"
        )
        ERROR_MIN_LENGTH = (
            "invalid length: expected length 32 for simple format, found {input_length}"
        )

        @classmethod
        def get_message_invalid_uuid(cls, char: str, position: int) -> str:
            return f"{cls.INVALID} {cls.ERROR_CHARACTER.format(char=char, position=position)}"

        @classmethod
        def get_message_min_length_uuid(cls, input_length: int) -> str:
            return f"{cls.INVALID} {cls.ERROR_MIN_LENGTH.format(input_length=input_length)}"

    class File:
        NOT_FOUND = "File not found"

    class Validation:
        STRING_TOO_SHORT = "String should have at least {min_length} character"
        STRING_TOO_LONG = "String should have at most {max_length} characters"

        @classmethod
        def get_string_too_short_msg(cls, min_length: int) -> str:
            base_msg = cls.STRING_TOO_SHORT.format(min_length=min_length)
            return base_msg + "s" if min_length != 1 else base_msg

        @classmethod
        def get_string_too_long_msg(cls, max_length: int) -> str:
            return cls.STRING_TOO_LONG.format(max_length=max_length)

    class Course:
        NOT_FOUND = "Course not found"

    class Exercise:
        NOT_FOUND = "Exercise not found"
