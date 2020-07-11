import requests
import json
import random



URL_CAT = 'http://127.0.0.1:8000/api/v1/services/servicecategories/'
URL_SER = 'http://127.0.0.1:8000/api/v1/services/all/'


def get_servicecategories():
    return json.loads(requests.get(URL_CAT).text)


def get_services(cat_id):
    url_servs = 'http://127.0.0.1:8000/api/v1/services/category/' + f'{cat_id}/'
    #url_servs = 'http://192.168.43.134/api/v1/services/category/' + f'{cat_id}/'
    print(url_servs)
    return json.loads(requests.get(url_servs).text)


def get_service(serv_id):
    url_serv = 'http://127.0.0.1:8000/api/v1/services/service/' + f'{serv_id}/'
    #url_serv = 'http://192.168.43.134/api/v1/services/service/' + f'{serv_id}/'
    print(url_serv)
    return json.loads(requests.get(url_serv).text)


def get_dates():
    url_dats = 'http://127.0.0.1:8000/api/v1/orders/dates/'
    #url_dats = 'http://192.168.43.134/api/v1/orders/dates/'
    print(url_dats)
    return json.loads(requests.get(url_dats).text)


def get_date(date_id):
    url_date = 'http://127.0.0.1:8000/api/v1/orders/date/' + f'{date_id}/'
    #url_date = 'http://192.168.43.134/api/v1/orders/date/' + f'{date_id}/'
    print(url_date)
    return json.loads(requests.get(url_date).text)


def get_periods():
    url_per = 'http://127.0.0.1:8000/api/v1/orders/periods/'
    #url_per = 'http://192.168.43.134/api/v1/orders/periods/'
    print(url_per)
    return json.loads(requests.get(url_per).text)


def get_period(per_id):
    url_per = 'http://127.0.0.1:8000/api/v1/orders/period/' + f'{per_id}/'
    #url_per = 'http://192.168.43.134/api/v1/orders/period/' + f'{per_id}/'
    print(url_per)
    return json.loads(requests.get(url_per).text)


def send_order(date_id, period_id, service_id, quantity):
    url_ordr = 'http://127.0.0.1:8000/api/v1/orders/create/order/'
    #url_ordr = 'http://192.168.43.134/api/v1/orders/create/order/'
    requests.post(url_ordr, data={'date': date_id, 'time_period': period_id, 'service_id': service_id, 'quantity': quantity})


def send_basket(date_id, period_id, service_id, token):
    url_bskt = 'http://127.0.0.1:8000/api/v1/orders/create/basket/'
    #url_bskt = 'http://192.168.43.134/api/v1/orders/create/basket/'
    headers = {'Authorization': 'Token ' + token}
    requests.post(url_bskt, headers=headers, data={
                                                  'date': date_id,
                                                   'time_period': period_id,
                                                   'service_id': service_id
    })


def get_basket(token):
    url_bskt = 'http://127.0.0.1:8000/api/v1/orders/basket/'
    #url_bskt = 'http://192.168.43.134/api/v1/orders/basket/'
    headers = {'Authorization': 'Token ' + token}
    print(url_bskt)
    return json.loads(requests.get(url_bskt, headers=headers).text)


def get_basket_for_card(token):
    url_bsk_all = 'http://127.0.0.1:8000/api/v1/orders/basket/all/'
    #url_bsk_all = 'http://192.168.43.134/api/v1/orders/basket/all/'
    print(url_bsk_all)
    headers = {'Authorization': 'Token ' + token}
    return json.loads(requests.get(url_bsk_all, headers=headers).text)


def clear_basket(bsk_id, token):
    url_bsk_clr = 'http://127.0.0.1:8000/api/v1/orders/basket/del/' + f'{bsk_id}/'
    #url_bsk_all = 'http://192.168.43.134/api/v1/orders/basket/all/'
    print(url_bsk_clr)
    headers = {'Authorization': 'Token ' + token}
    requests.delete(url_bsk_clr, headers=headers)


def create_card(token):
    url_card = 'http://127.0.0.1:8000/api/v1/orders/create/card/'
    #url_card = 'http://192.168.43.134/api/v1/orders/create/card/'
    print(url_card)
    card_items = []
    basket = get_basket_for_card(token)
    for item in basket:
        card_items.append(item)
        bsk_id = item['id']
        clear_basket(bsk_id, token)
    print(card_items)
    card_number = random.randint(1000, 9999)
    payload = {'card_items': card_items, 'card_number': card_number}
    headers = {'Authorization': 'Token ' + token}
    requests.post(url_card, headers=headers, json=payload)


def get_card(crd_n, token):
    url_card = 'http://127.0.0.1:8000/api/v1/orders/card/' + f'{crd_n}/'
    #url_card = 'http://192.168.43.134/api/v1/orders/card/' + f'{crd_n}/'
    headers = {'Authorization': 'Token ' + token}

    return json.loads(requests.get(url_card, headers=headers).text)


def get_cards_nums(token):
    url_cards = 'http://127.0.0.1:8000/api/v1/orders/card/all/'
    #url_cards = 'http://192.168.43.134/api/v1/orders/card/all/'
    headers = {'Authorization': 'Token ' + token}
    return json.loads(requests.get(url_cards, headers=headers).text)


def make_reg(email, password):
    url_reg = 'http://127.0.0.1:8000/api/v1/rest-auth/registration/'
    #url_reg = 'http://192.168.43.134/api/v1/rest-auth/registration/'
    requests.post(url_reg, data={'email': email, 'password1': password, 'password2': password})


def get_token_login(email, password):
    url_tok = 'http://127.0.0.1:8000/api/v1/rest-auth/login/'
    #url_tok = 'http://192.168.43.134/api/v1/rest-auth/login/'
    result = requests.post(url_tok, data={'email': email, 'password': password})
    return json.loads(result.text)


def token_logout(token):
    url_out = 'http://127.0.0.1:8000/api/v1/rest-auth/logout/'
    #url_out = 'http://192.168.43.134/api/v1/rest-auth/logout/'
    headers = {'Authorization': 'Token ' + token}
    requests.post(url_out, headers=headers)





def make_active(crd_n, token):
    url_act = 'http://127.0.0.1:8000/api/v1/orders/card/' + f'{crd_n}' + '/activate/'
    #url_act = 'http://192.168.43.134/api/v1/orders/card/' + f'{crd_n}' + '/activate/'
    headers = {'Authorization': 'Token ' + token}
    requests.put(url_act, data={'is_active': True}, headers=headers)


def send_email(email):
    url_email = 'http://127.0.0.1:8000/api/v1/orders/email/' + f'{email}/'
    #url_email = 'http://192.168.43.134/api/v1/orders/email/' + f'{email}/'
    requests.get(url_email)


if __name__ == '__main__':
    res = get_token_login('spoliv@rambler.ru', 'geekbrains')
    # res = make_reg('spoliv@rambler.ru', 'geekbrains')
    print(res['key'])
    #make_reg('spoliv@rambler.ru', 'geekbrains')