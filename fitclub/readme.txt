http://127.0.0.1:8000/api/v1/users/<token>/


{
	'update_id': 813718940,
	'message': {
				'message_id': 79,
				'from': {
						'id': 736041685,
						'is_bot': False,
						'first_name': 'Oleg',
						'last_name': 'Sp',
						'language_code': 'ru'
						},
				'chat': {
						'id': 736041685,
						'first_name': 'Oleg',
						'last_name': 'Sp',
						'type': 'private'
						},
				'date': 1589628849,
				'text': 'help'
				}
}

https://api.telegram.org/bot1<token>/getMe

в ответ получаем
{"ok":true,"result":{"id":1168528589,"is_bot":true,"first_name":"FitClubBot",
                     "username":"sp_fit_bot","can_join_groups":true,"can_read_all_group_messages":false,
                     "supports_inline_queries":false}}


https://api.telegram.org/bot<token>/getUpdates

в ответ получакм

{"ok":true,"result":[{"update_id":813718941,
"message":{"message_id":83,"from":{"id":736041685,"is_bot":false,"first_name":"Oleg","last_name":"Sp","language_code":"ru"},"chat":{"id":736041685,"first_name":"Oleg","last_name":"Sp","type":"private"},"date":1589816866,"text":"/start","entities":[{"offset":0,"length":6,"type":"bot_command"}]}},{"update_id":813718942,
"message":{"message_id":85,"from":{"id":736041685,"is_bot":false,"first_name":"Oleg","last_name":"Sp","language_code":"ru"},"chat":{"id":736041685,"first_name":"Oleg","last_name":"Sp","type":"private"},"date":1589823830,"text":"\u041f\u0440\u0438\u0432\u0435 \u0431\u043e\u0442"}}]}


http://127.0.0.1:8000/api/v1/services/create/category/
http://127.0.0.1:8000/api/v1/services/create/service/
http://127.0.0.1:8000/api/v1/services/category/1/
http://127.0.0.1:8000/api/v1/services/all/

http://127.0.0.1:8000/api/v1/orders/create/date/
http://127.0.0.1:8000/api/v1/orders/create/period/
http://127.0.0.1:8000/api/v1/orders/create/order/
http://127.0.0.1:8000/api/v1/orders/order/1/3/4/

http://127.0.0.1:8000/api/v1/orders/dates/
http://127.0.0.1:8000/api/v1/orders/create/card/
http://127.0.0.1:8000/api/v1/orders/create/card_item/
http://127.0.0.1:8000/api/v1/orders/all/1/336/
http://127.0.0.1:8000/api/v1/orders/card_items/all/

http://127.0.0.1:8000/api/v1/orders/create/basket/
http://127.0.0.1:8000/api/v1/orders/basket/2/
http://127.0.0.1:8000/api/v1/orders/basket/2/all/

http://127.0.0.1:8000/api/v1/orders/basket/last/2/

{"card_items": [{"date": 4, "time_period": 5, "service_id": 8},
                {"date": 1, "time_period": 3, "service_id": 5}],
                "user": 1, "card_number": 333}