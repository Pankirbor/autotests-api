from http import HTTPStatus

import allure
from allure_commons.types import Severity
import pytest

from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
)
from clients.users.constants import MAX_LENGTH_FIELDS
from clients.users.public_users_client import PublicUsersClient
from clients.users.private_users_client import PrivateUsersClient
from clients.users.users_schema import (
    CreateUserRequestSchema,
    UpdateUserRequestSchema,
    UserResponseSchema,
)
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.schema import validate_json_schema
from tools.assertions.base import assert_status_code
from tools.assertions.users import (
    assert_create_or_update_user_with_empty_required_field_response,
    assert_create_or_update_user_with_too_long_field_response,
    assert_create_user_response,
    assert_delete_user_with_incorrect_user_id_response,
    assert_get_user_response,
    assert_get_user_with_incorrect_user_id_response,
    assert_not_found_user_response,
    assert_update_user_response,
    assert_user,
)
from tools.console_output_formatter import print_dict
from tools.fakers import fake


@pytest.mark.regression
@pytest.mark.users
@allure.tag(AllureTag.USERS, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.parent_suite(AllureEpic.LMS)
@allure.feature(AllureFeature.USERS)
@allure.suite(AllureFeature.USERS)
class TestUsers:
    """Тесты для работы с users эндпоинтами API."""

    @pytest.mark.parametrize("email", ["gmail.com", "mail.ru", "example.com"])
    @allure.tag(AllureTag.CREATE_ENTITY)
    @allure.story(AllureStory.CREATE_ENTITY)
    @allure.sub_suite(AllureStory.CREATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Create user")
    def test_create_user(
        self,
        public_users_client: PublicUsersClient,
        email: str,
    ):
        """Тест создания пользователя.

        Args:
            public_users_client (PublicUsersClient): Клиент для работы с публичными users эндпоинтами API.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.OK.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            ValidationError: Если данные ответа не соответствуют схеме.
        """

        request = CreateUserRequestSchema(email=fake.email(email))
        response = public_users_client.create_user_api(request)
        response_data = UserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_create_user_response(request, response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Get user me")
    def test_get_user_me(
        self,
        private_users_client: PrivateUsersClient,
        function_user: UserFixture,
    ):
        """
        Тест получения информации о пользователе по url users/me.

        Args:
            private_users_client (PrivateUsersClient): Клиент для работы с закрытыми users эндпоинтами API.
            function_user (UserFixture): Объект с данными созданного пользователя.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.OK.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            ValidationError: Если данные ответа не соответствуют схеме.
        """
        response = private_users_client.get_user_me_api()
        response_data = UserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_get_user_response(response_data.user, function_user.response.user)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.GET_ENTITY)
    @allure.story(AllureStory.GET_ENTITY)
    @allure.sub_suite(AllureStory.GET_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Get user by id")
    def test_get_user_by_id(
        self, private_users_client: PrivateUsersClient, function_user: UserFixture
    ):
        """
        Тест получения информации о пользователе по url users/{user_id}.

        Args:
            private_users_client (PrivateUsersClient): Клиент для работы с закрытыми users эндпоинтами API.
            function_user (UserFixture): Объект с данными созданного пользователя.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.OK.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            ValidationError: Если данные ответа не соответствуют схеме.
        """
        response = private_users_client.get_user_api(function_user.user_id)
        response_data = UserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_user(actual=response_data.user, expected=function_user.response.user)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Get a non-existent user")
    def test_get_non_existent_user(self, private_users_client: PrivateUsersClient):
        """
        Тест получения информации о несуществующем пользователе.

        Args:
            private_users_client (PrivateUsersClient): Клиент для работы с закрытыми users эндпоинтами API.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.NOT_FOUND.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            ValidationError: Если данные ответа не соответствуют схеме.
        """

        response = private_users_client.get_user_api(user_id=fake.uuid4())
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.NOT_FOUND)
        assert_not_found_user_response(actual=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Get user with invalid id")
    def test_get_user_with_invalid_id(self, private_users_client: PrivateUsersClient):
        """
        Тест получения информации о пользователе с некорректным id.

        Args:
            private_users_client (PrivateUsersClient): Клиент для работы с закрытыми users эндпоинтами API.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.UNPROCESSABLE_ENTITY.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            ValidationError: Если данные ответа не соответствуют схеме.
        """

        response = private_users_client.get_user_api(user_id="incorrect-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_get_user_with_incorrect_user_id_response(actual=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.UPDATE_ENTITY)
    @allure.story(AllureStory.UPDATE_ENTITY)
    @allure.sub_suite(AllureStory.UPDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Update user")
    def test_update_user(
        self,
        private_users_client: PrivateUsersClient,
        function_user: UserFixture,
    ):
        """
        Тест обновления информации о пользователе.

        Args:
            private_users_client (PrivateUsersClient): Клиент для работы с закрытыми users эндпоинтами API.
            function_user (UserFixture): Объект с данными созданного пользователя.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.OK.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            ValidationError: Если данные ответа не соответствуют схеме.
        """
        request = UpdateUserRequestSchema()
        response = private_users_client.update_user_api(
            request=request, user_id=function_user.user_id
        )
        response_data = UserResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_update_user_response(response_data, request, function_user.user_id)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.tag(AllureTag.DELETE_ENTITY)
    @allure.story(AllureStory.DELETE_ENTITY)
    @allure.sub_suite(AllureStory.DELETE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Delete user")
    def test_delete_user(
        self,
        private_users_client: PrivateUsersClient,
        public_users_client: PublicUsersClient,
    ):
        """
        Тест удаления пользователя.

        Args:
            private_users_client (PrivateUsersClient): Клиент для работы с закрытыми users эндпоинтами API.
            public_users_client (PublicUsersClient): Клиент для работы с публичными users эндпоинтами API.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.OK.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            AssertError: Если данные ответа не соответствуют ожидаемым.
        """
        created_user = public_users_client.create_user(
            request=CreateUserRequestSchema()
        )
        delete_response = private_users_client.delete_user_api(created_user.user.id)
        assert_status_code(delete_response.status_code, HTTPStatus.OK)

        not_found_response = private_users_client.get_user_api(created_user.user.id)
        not_found_response_data = InternalErrorResponseSchema.model_validate_json(
            not_found_response.text
        )
        assert_status_code(not_found_response.status_code, HTTPStatus.NOT_FOUND)
        assert_not_found_user_response(actual=not_found_response_data)

        validate_json_schema(
            not_found_response.json(), not_found_response_data.model_json_schema()
        )

    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.NORMAL)
    @allure.title("Delete user with invalid id")
    def test_delete_user_with_invalid_id(
        self, private_users_client: PrivateUsersClient
    ):
        """
        Тест удаления пользователя с некорректным id.

        Args:
            private_users_client (PrivateUsersClient): Клиент для работы с закрытыми users эндпоинтами API.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.UNPROCESSABLE_ENTITY.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            ValidationError: Если данные ответа не соответствуют схеме.
        """

        response = private_users_client.delete_user_api(user_id="incorrect-id")
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_delete_user_with_incorrect_user_id_response(actual=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize(
        "field_name", ["email", "first_name", "last_name", "middle_name"]
    )
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Create user with empty required string fields")
    def test_create_user_with_empty_required_string_fields(
        self,
        public_users_client: PublicUsersClient,
        field_name: str,
    ):
        """
        Тест создания пользователя с пустым обязательным полем.

        Args:
            public_users_client (PublicUsersClient): Клиент для работы с публичными users эндпоинтами API.
            field_name (str): Имя поля, которое будет содержать пустое значение в запросе.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.UNPROCESSABLE_ENTITY.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            ValidationError: Если данные ответа не соответствуют схеме.
        """

        request = CreateUserRequestSchema()
        setattr(request, field_name, "")

        allure.dynamic.title(f"Attempt create user with empty {field_name} field")
        response = public_users_client.create_user_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)
        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_or_update_user_with_empty_required_field_response(
            actual=response_data, field_name=field_name
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize(
        "field_name", ["email", "first_name", "last_name", "middle_name"]
    )
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Update user with empty required string fields")
    def test_update_user_with_empty_required_string_fields(
        self,
        private_users_client: PrivateUsersClient,
        function_user: UserFixture,
        field_name: str,
    ):
        """
        Тест обновления пользователя с пустым обязательным полем.

        Args:
            private_users_client (PrivateUsersClient): Клиент для работы с закрытыми users эндпоинтами API.
            function_user (UserFixture): Объект с данными созданного пользователя.
            field_name (str): Имя поля, которое будет содержать пустое значение в запросе.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.UNPROCESSABLE_ENTITY.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            ValidationError: Если данные ответа не соответствуют схеме.
        """

        request = UpdateUserRequestSchema()
        setattr(request, field_name, "")

        allure.dynamic.title(f"Attempt update user with empty {field_name} field")
        response = private_users_client.update_user_api(
            request=request, user_id=function_user.user_id
        )
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_or_update_user_with_empty_required_field_response(
            actual=response_data, field_name=field_name
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize(
        "field_name", ["email", "first_name", "last_name", "middle_name"]
    )
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Create user with too long string fields")
    def test_create_user_with_too_long_string_fields(
        self,
        public_users_client: PublicUsersClient,
        field_name: str,
    ):
        """
        Тест создания пользователя со значением, превышающим максимальную длину поля.

        Args:
            public_users_client (PublicUsersClient): Клиент для работы с публичными users эндпоинтами API.
            field_name (str): Имя поля, которое будет содержать слишком длинное значение в запросе.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.UNPROCESSABLE_ENTITY.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            ValidationError: Если данные ответа не соответствуют схеме.
        """

        too_long_string = "a" * (MAX_LENGTH_FIELDS.get(field_name) + 1)
        request = CreateUserRequestSchema()
        setattr(request, field_name, too_long_string)

        allure.dynamic.title(
            f"Attempt create user with to long value in {field_name} field"
        )
        response = public_users_client.create_user_api(request=request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_or_update_user_with_too_long_field_response(
            actual=response_data, field_name=field_name, input_val=too_long_string
        )

        validate_json_schema(response.json(), response_data.model_json_schema())

    @pytest.mark.parametrize(
        "field_name", ["email", "first_name", "last_name", "middle_name"]
    )
    @allure.tag(AllureTag.VALIDATE_ENTITY)
    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.CRITICAL)
    @allure.title("Update user with too long string fields")
    def test_update_user_with_too_long_string_fields(
        self,
        private_users_client: PrivateUsersClient,
        function_user: UserFixture,
        field_name: str,
    ):
        """
        Тест обновления пользователя со значением, превышающим максимальную длину поля.

        Args:
            private_users_client (PrivateUsersClient): Клиент для работы с закрытыми users эндпоинтами API.
            function_user (UserFixture): Объект с данными созданного пользователя.
            field_name (str): Имя поля, которое будет содержать слишком длинное значение в запросе.

        Raises:
            AssertionError: Если статус код ответа не равен HTTPStatus.UNPROCESSABLE_ENTITY.
            AssertionError: Если данные ответа не соответствуют ожидаемым.
            ValidationError: Если данные ответа не соответствуют схеме.
        """

        too_long_string = "a" * (MAX_LENGTH_FIELDS.get(field_name) + 1)
        request = UpdateUserRequestSchema()
        setattr(request, field_name, too_long_string)

        allure.dynamic.title(
            f"Attempt update user with to long value in {field_name} field"
        )
        response = private_users_client.update_user_api(
            request=request, user_id=function_user.user_id
        )
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_create_or_update_user_with_too_long_field_response(
            actual=response_data, field_name=field_name, input_val=too_long_string
        )

        validate_json_schema(response.json(), response_data.model_json_schema())
