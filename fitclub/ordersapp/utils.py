import requests
import json


def get_dates():
    url_dat = 'http://127.0.0.1:8000/api/v1/orders/dates/'
    print(url_dat)
    return json.loads(requests.get(url_dat).text)


def get_periods():
    url_per = 'http://127.0.0.1:8000/api/v1/orders/periods/'
    print(url_per)
    return json.loads(requests.get(url_per).text)


list_a = [1, 2, 3, 4]

map(str, list_a)
#
for l_item in list_a:
    print(type(l_item))

print(''.join(map(str, list_a)))
