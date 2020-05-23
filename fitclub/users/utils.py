
import re
import requests
import json

URL = 'http://127.0.0.1:8000/api/v1/users/'


def get_users():
    return json.loads(requests.get(URL).text)

print(get_users())











# from .models import ClubClient
#
#
# def get_users():
#     return ClubClient.objects.all()

