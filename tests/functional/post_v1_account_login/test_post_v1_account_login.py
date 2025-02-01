import allure

from checkers.http_checkers import check_status_code_http


@allure.suite("Тест на проверку метода POST:v1/account/login")
class TestPostV1AccountLogin:

    @allure.sub_suite("Негативные тесты")
    @allure.title("Проверка логина неактивного пользователя")
    def test_post_v1_account_login_not_activated_user(self, account_helper, prepared_user):
        login = prepared_user.login
        password = prepared_user.password
        email = prepared_user.email
        account_helper.create_user(email=email, login=login, password=password)
        with check_status_code_http(
                expected_status_code=403,
                expected_title="User is inactive. Address the technical support for more details"
        ):
            response = account_helper.login_user_raw(login=login, password=password)
