import requests
import json
import random



URL_CAT = 'http://127.0.0.1:8000/api/v1/services/servicecategories/'
URL_SER = 'http://127.0.0.1:8000/api/v1/services/all/'


def get_servicecategories():
    return json.loads(requests.get(URL_CAT).text)


#print(get_servicecategories())

def get_services(cat_id):
    url_servs = 'http://127.0.0.1:8000/api/v1/services/category/' + f'{cat_id}/'
    print(url_servs)
    return json.loads(requests.get(url_servs).text)


def get_service(serv_id):
    url_serv = 'http://127.0.0.1:8000/api/v1/services/service/' + f'{serv_id}/'
    print(url_serv)
    return json.loads(requests.get(url_serv).text)


def get_dates():
    url_dats = 'http://127.0.0.1:8000/api/v1/orders/dates/'
    print(url_dats)
    return json.loads(requests.get(url_dats).text)


def get_date(date_id):
    url_date = 'http://127.0.0.1:8000/api/v1/orders/date/' + f'{date_id}/'
    print(url_date)
    return json.loads(requests.get(url_date).text)


def get_periods():
    url_per = 'http://127.0.0.1:8000/api/v1/orders/periods/'
    print(url_per)
    return json.loads(requests.get(url_per).text)


def get_period(per_id):
    url_per = 'http://127.0.0.1:8000/api/v1/orders/period/' + f'{per_id}/'
    print(url_per)
    return json.loads(requests.get(url_per).text)


def send_order(date_id, period_id, service_id, quantity):
    url_ordr = 'http://127.0.0.1:8000/api/v1/orders/create/order/'
    requests.post(url_ordr, data={'date': date_id, 'time_period': period_id, 'service_id': service_id, 'quantity': quantity})


def send_basket(date_id, period_id, service_id, user_id):
    url_bskt = 'http://127.0.0.1:8000/api/v1/orders/create/basket/'
    requests.post(url_bskt, data={'user': user_id, 'date': date_id, 'time_period': period_id, 'service_id': service_id})


def get_basket(usr_id):
    url_bskt = 'http://127.0.0.1:8000/api/v1/orders/basket/' + f'{usr_id}/'
    print(url_bskt)
    return json.loads(requests.get(url_bskt).text)


def get_basket_for_card(usr_id):
    url_bskt = 'http://127.0.0.1:8000/api/v1/orders/basket/' + f'{usr_id}/' + 'all/'
    print(url_bskt)
    return json.loads(requests.get(url_bskt).text)


#def create_card(usr_id, card_number):
def create_card(usr_id):
    url_card = 'http://127.0.0.1:8000/api/v1/orders/create/card/'
    print(url_card)
    card_items = []
    basket = get_basket_for_card(usr_id)
    for item in basket:
        card_items.append(item)
    print(card_items)
    card_number = random.randint(1000, 9999)
    #requests.post(url_card, data={'card_items': card_items, 'user': usr_id, 'card_number': card_number})
    payload = {'card_items': card_items, 'user': usr_id, 'card_number': card_number}
    #payload = {'card_items': card_items, 'user': usr_id}
    requests.post(url_card, json=payload)


def get_card(crd_n):
    url_card = 'http://127.0.0.1:8000/api/v1/orders/card/' + f'{crd_n}/'
    return json.loads(requests.get(url_card).text)

# def get_basket_last(usr_id):
#     url_bskt_ls = 'http://127.0.0.1:8000/api/v1/orders/basket/last/' + f'{usr_id}/'
#     print(url_bskt_ls)
#     return json.loads(requests.get(url_bskt_ls).text)