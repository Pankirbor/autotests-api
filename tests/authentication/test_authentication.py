from http import HTTPStatus

import allure
from allure_commons.types import Severity
import pytest

from clients.authentication.authentication_client import AuthenticationClient
from clients.authentication.authentication_schema import (
    LoginRequestSchema,
    LoginResponseSchema,
)

from fixtures.users import UserFixture
from tools.allure.epics import AllureEpic
from tools.allure.features import AllureFeature
from tools.allure.stories import AllureStory
from tools.allure.tags import AllureTag
from tools.assertions.authentication import assert_login_response
from tools.assertions.base import assert_status_code
from tools.assertions.schema import validate_json_schema


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
