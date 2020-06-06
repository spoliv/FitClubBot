import telepot


token = '1168528589:AAFieV61wqq_aDgmeeCNykGIFVt3d1KvGxk'
TelegramBot = telepot.Bot(token)
#print(TelegramBot.getMe())
#print(TelegramBot.getUpdates(813718936+1))
print(TelegramBot.getUpdates())



# Это нужно прописать в контроллере (viewer)

# import telepot
# import json
# from django.template.loader import render_to_string
# from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse
# from django.views.generic import View
# from django.views.decorators.csrf import csrf_exempt
# from django.utils.decorators import method_decorator
# #from mainfitclub.mainfitclub import settings
#
#
# from .utils import get_users
#
#
# token = '1168528589:AAFieV61wqq_aDgmeeCNykGIFVt3d1KvGxk'
# TelegramBot = telepot.Bot(token)
# #TelegramBot.setWebhook('https://127.0.0.1:8000/api/v1/users/{bot_token}/'.format(bot_token=token))
#
# def _display_help():
#     return render_to_string('help.md')
#     #return render_to_string('help goes')
#
# # def _display_planetpy_feed():
# #     return render_to_string('feed.md', {'items': parse_planetpy_rss()})
# def _display_users():
#     return render_to_string('users.md', {'items': get_users()})
#
# class CommandReceiveView(View):
#     def post(self, request, bot_token):
#         if bot_token != token:
#             return HttpResponseForbidden('Invalid token')
#         commands = {
#             '/start': _display_help,
#             'help': _display_help,
#             #'feed': _display_planetpy_feed,
#             'users': _display_users,
#         }
#         try:
#             payload = json.loads(request.body.decode('utf-8'))
#         except ValueError:
#             return HttpResponseBadRequest('Invalid request body')
#         else:
#             chat_id = payload['message']['chat']['id']
#             cmd = payload['message'].get('text')  # command
#             func = commands.get(cmd.split()[0].lower())
#             if func:
#                 TelegramBot.sendMessage(chat_id, func(), parse_mode='Markdown')
#             else:
#                 TelegramBot.sendMessage(chat_id, 'I do not understand you, Sir!')
#         return JsonResponse({}, status=200)
#     @method_decorator(csrf_exempt)
#     def dispatch(self, request, *args, **kwargs):
#         return super(CommandReceiveView, self).dispatch(request, *args, **kwargs)
