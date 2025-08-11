from http import HTTPStatus

import allure
from allure_commons.types import Severity
import pytest

from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import (
    LoginRequestSchema,
    LoginResponseSchema,
    RefreshRequestSchema,
)

from clients.errors_schema import (
    InternalErrorResponseSchema,
    ValidationErrorResponseSchema,
)
from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.authentication import (
    assert_login_response,
    assert_login_with_incorrect_email_response,
    assert_refresh_token_with_incorrect_token_response,
)
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema
from tools.console_output_formatter import print_dict


@pytest.mark.authentication
@pytest.mark.regression
@allure.tag(AllureTag.AUTHENTICATION, AllureTag.REGRESSION)
@allure.epic(AllureEpic.LMS)
@allure.parent_suite(AllureEpic.LMS)
@allure.feature(AllureFeature.AUTHENTICATION)
@allure.suite(AllureFeature.AUTHENTICATION)
class TestAuthentication:
    """Тесты для проверки API аутентификации."""

    @allure.story(AllureStory.LOGIN)
    @allure.sub_suite(AllureStory.LOGIN)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Login with correct email and password")
    def test_login(
        self,
        function_user: UserFixture,
        authentication_client: AuthenticationClient,
    ):
        """
        Тест проверки аутентификации пользователя.

        Args:
            function_user (UserFixture): Пользователь для аутентификации.
            authentication_client (AuthenticationClient): Клиент для работы с аутентификацией.

        Raises:
            AssertionError: Если статус ответа не 200 OK или данные ответа не соответствуют ожиданиям.
            ValidationError: Если данные ответа не соответствуют схеме LoginResponseSchema.
        """

        request = LoginRequestSchema(
            email=function_user.email, password=function_user.password
        )
        response = authentication_client.login_api(request)
        response_data = LoginResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.OK)
        assert_login_response(response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(AllureStory.LOGIN)
    @allure.sub_suite(AllureStory.LOGIN)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Refresh token with correct token")
    def test_refresh_token(
        self,
        function_user: UserFixture,
        authentication_client: AuthenticationClient,
    ):
        login_request = LoginRequestSchema(
            email=function_user.email, password=function_user.password
        )
        login_response = authentication_client.login(login_request)
        refresh_request = RefreshRequestSchema(
            refresh_token=login_response.token.refresh_token
        )
        refresh_response = authentication_client.refresh_api(refresh_request)
        refresh_response_data = LoginResponseSchema.model_validate_json(
            refresh_response.text
        )

        assert_status_code(refresh_response.status_code, HTTPStatus.OK)
        assert_login_response(refresh_response_data)

        validate_json_schema(
            refresh_response.json(), refresh_response_data.model_json_schema()
        )

    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Refresh token with incorrect token")
    def test_refresh_token_with_incorrect_token(
        self, authentication_client: AuthenticationClient
    ):
        """
        Тест проверки обновления токена с некорректным токеном.

        Args:
            authentication_client (AuthenticationClient): Клиент для работы с аутентификацией.

        Raises:
            AssertionError: Если статус ответа не 422 UNPROCESSABLE_ENTITY или данные ответа не соответствуют ожиданиям.
            ValidationError: Если данные ответа не соответствуют схеме ValidationErrorResponseSchema.
        """

        response = authentication_client.refresh_api(
            RefreshRequestSchema(refresh_token="incorrect-token")
        )
        response_data = InternalErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNAUTHORIZED)
        assert_refresh_token_with_incorrect_token_response(actual=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())

    @allure.story(AllureStory.VALIDATE_ENTITY)
    @allure.sub_suite(AllureStory.VALIDATE_ENTITY)
    @allure.severity(Severity.BLOCKER)
    @allure.title("Login with incorrect email")
    def test_login_with_incorrect_email(
        self, authentication_client: AuthenticationClient
    ):
        request = LoginRequestSchema(email="", password="password")
        response = authentication_client.login_api(request)
        response_data = ValidationErrorResponseSchema.model_validate_json(response.text)

        assert_status_code(response.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        assert_login_with_incorrect_email_response(actual=response_data)

        validate_json_schema(response.json(), response_data.model_json_schema())
