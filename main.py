'''
curl -X 'POST' \
  'http://5.63.153.31:5051/v1/account' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "login": "test_new",
  "email": "test@mail.ru",
  "password": "test"
}
'''

import requests

# url = "http://5.63.153.31:5051/v1/account"
# headers = {"accept": "*/*", "Content-Type": "application/json", }
# payload = {"login": "test_new", "email": "test@mail.ru", "password": "test1234"}
# response = requests.post(url=url, headers=headers, json=payload)
#
# print(response.status_code)
# pprint.pprint(response.json())

url = "http://5.63.153.31:5051/v1/account/5cdd7e97-af35-435e-96e7-97b03bc7b760"
headers = {
    "accept": "text/plain", }
response = requests.put(url=url, headers=headers)

print(f"{response.status_code}")
response_json = response.json()
print(response_json["resource"]["rating"]["quantity"])
