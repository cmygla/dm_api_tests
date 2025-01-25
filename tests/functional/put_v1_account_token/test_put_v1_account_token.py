import uuid


def test_put_v1_account_token_not_valid(account_helper):
    # активация  с невалидным токеном
    token = str(uuid.uuid4())
    response = account_helper.dm_api_account.account_api.put_v1_account_token(
        token=token, validate_response=False
    )
    assert response.status_code == 410, "Пользователь был активирован с невалидным токеном"
