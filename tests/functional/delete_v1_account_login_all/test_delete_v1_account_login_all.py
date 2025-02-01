import allure


@allure.suite("Тест на проверку метода DELETE:v1/account/login/all")
class TestDeleteV1AccountLoginAll:

    @allure.sub_suite("Позитивные тесты")
    @allure.title("Проверка логаута пользователя на всех устройствах")
    def test_delete_v1_account_login_all(self, auth_account_helper):
        auth_account_helper.delete_acсount_login_all()
