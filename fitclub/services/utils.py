import requests
import json

URL_CAT = 'http://127.0.0.1:8000/api/v1/services/servicecategories/'
URL_SER = 'http://127.0.0.1:8000/api/v1/services/all/'


def get_servicecategories():
    return json.loads(requests.get(URL_CAT).text)


#print(get_servicecategories())

def get_services(cat_id):
    url_ser = 'http://127.0.0.1:8000/api/v1/services/category/' + f'{cat_id}/'
    print(url_ser)
    return json.loads(requests.get(url_ser).text)
