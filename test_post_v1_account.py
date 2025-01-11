import requests


def test_post_v1_account():
    login = 'user_ekv'
    password = 'user_ekv_123'
    email = f'{login}@mail.ru'
    # регистрация пользователя
    json_data = {'login': login, 'email': email, 'password': password, }
    response = requests.post('http://5.63.153.31:5051/v1/account', json=json_data)

    print(response.status_code)
    print(response.json())

    # получение письма из почтового сервера
    params = {'limit': '50', }
    response = requests.get('http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    print(response.json())

    # получение активационного токена

    # активация пользователя
    response = requests.put('http://5.63.153.31:5051/v1/account/9e597120-726f-4b99-b6fc-7023f1a39d36')
    print(response.status_code)
    print(response.json())

    # авторизация
    json_data = {'login': login, 'password': password, 'rememberMe': True, }
    response = requests.post('http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    print(response.json())
