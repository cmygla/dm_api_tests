import uuid


def test_put_v1_account_token_not_valid(account_api):
    # активация  с невалидным токеном
    token = str(uuid.uuid4())
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 410, "Пользователь был активирован с невалидным токеном"
