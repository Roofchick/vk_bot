import requests

from func.regular import *

def status(STATUS, TOKEN, BotID, regulars, count_message, start_bot):
	status = regular(STATUS, BotID, count_message, start_bot, TOKEN, regulars)
	st = requests.post('https://api.vk.com/method/status.set', params = {'access_token': TOKEN, 'v': 5.21, 'text': status})