import uuid

from conftest import account_helper


def test_put_v1_account_token_not_valid():
    # активация  с невалидным токеном
    token = str(uuid.uuid4())
    response = account_helper.dm_api_account.account_api.put_v1_account_token(token=token)
    assert response.status_code == 410, "Пользователь был активирован с невалидным токеном"
