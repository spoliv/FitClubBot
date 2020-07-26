import requests
import json
import random
from myfitbot.request_urls import *


def get_servicecategories():
    return json.loads(requests.get(url_cat).text)


def get_services(cat_id):
    return json.loads(requests.get(url_servs + f'{cat_id}/').text)


def get_service(serv_id):
    return json.loads(requests.get(url_serv + f'{serv_id}/').text)


def create_date(date_name):
    requests.post(url_crt_date,
                  data={'date': date_name})


def get_dates():
    return json.loads(requests.get(url_dats).text)


def get_date(date_id):
    return json.loads(requests.get(url_date + f'{date_id}/').text)


def get_periods():
    return json.loads(requests.get(url_pers).text)


def get_period(per_id):
    return json.loads(requests.get(url_per + f'{per_id}/').text)


def send_order(date_id, period_id, service_id, quantity):
    requests.post(url_ordr, data={'date': date_id, 'time_period': period_id, 'service_id': service_id, 'quantity': quantity})


def send_basket(date_id, period_id, service_id, token):
    headers = {'Authorization': 'Token ' + token}
    requests.post(url_bskt, headers=headers, data={
                                                  'date': date_id,
                                                   'time_period': period_id,
                                                   'service_id': service_id
    })


def get_basket(token):
    headers = {'Authorization': 'Token ' + token}
    return json.loads(requests.get(url_baskt, headers=headers).text)


def get_basket_for_card(token):
    headers = {'Authorization': 'Token ' + token}
    return json.loads(requests.get(url_bsk_all, headers=headers).text)


def clear_basket(bsk_id, token):
    headers = {'Authorization': 'Token ' + token}
    requests.delete(url_bsk_clr + f'{bsk_id}/', headers=headers)


def create_card(token):
    card_items = []
    basket = get_basket_for_card(token)
    for item in basket:
        card_items.append(item)
        bsk_id = item['id']
        clear_basket(bsk_id, token)
    card_number = random.randint(1000, 9999)
    payload = {'card_items': card_items, 'card_number': card_number}
    headers = {'Authorization': 'Token ' + token}
    requests.post(url_crt_card, headers=headers, json=payload)


def get_card(crd_n, token):
    headers = {'Authorization': 'Token ' + token}

    return json.loads(requests.get(url_card + f'{crd_n}/', headers=headers).text)


def get_cards_nums(token):
    headers = {'Authorization': 'Token ' + token}
    return json.loads(requests.get(url_cards, headers=headers).text)


def make_reg(email, password):
    requests.post(url_reg, data={'email': email, 'password1': password, 'password2': password})


def get_token_login(email, password):
    result = requests.post(url_tok, data={'email': email, 'password': password})
    return json.loads(result.text)


def token_logout(token):
    headers = {'Authorization': 'Token ' + token}
    requests.post(url_out, headers=headers)


def make_active(crd_n, token):
    headers = {'Authorization': 'Token ' + token}
    requests.put(url_act + f'{crd_n}/', data={'is_active': True}, headers=headers)


def send_email(email):
    requests.get(url_email + f'{email}/')


