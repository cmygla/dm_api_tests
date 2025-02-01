import allure


@allure.suite("Тест на проверку метода DELETE:v1/account/login")
class TestDeleteV1AccountLogin:

    @allure.sub_suite("Позитивные тесты")
    @allure.title("Проверка логаута пользователя")
    def test_delete_v1_account_login(self, auth_account_helper):
        auth_account_helper.delete_account_login()
