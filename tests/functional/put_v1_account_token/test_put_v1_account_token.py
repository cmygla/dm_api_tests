import uuid

from checkers.http_checkers import check_status_code_http


def test_put_v1_account_token_not_valid(account_helper):
    # активация  с невалидным токеном
    token = str(uuid.uuid4())
    with check_status_code_http(
            expected_status_code=410,
            expected_title="Activation token is invalid! Address the technical support for further assistance"
    ):
        response = account_helper.dm_api_account.account_api.put_v1_account_token(token=token)
