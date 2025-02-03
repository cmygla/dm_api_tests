import allure


@allure.suite("Тест на проверку метода PUT:v1/account/password")
class TestPutV1AccountPassword:
    @allure.sub_suite("Позитивные тесты")
    @allure.title("Проверка смены пароля активного пользователя")
    def test_put_v1_account_password(self, mailhog_helper, account_helper, prepared_user):
        login = prepared_user.login
        password = prepared_user.password
        email = prepared_user.email
        new_password = f'{password}_'
        account_helper.auth_client(email=email, login=login, password=password)
        account_helper.change_account_password(email=email, login=login, old_pass=password, new_pass=new_password)
        account_helper.login_user_raw(login=login, password=new_password)
