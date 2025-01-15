from conftest import account_helper


def test_post_v1_account(test_data):
    account_helper.register_new_user(email=test_data["email"], login=test_data["login"], password=test_data["password"])
    account_helper.login_user(login=test_data["login"], password=test_data["password"])
