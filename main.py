try:
	import requests, json, random, time, string, threading, textwrap
	from PIL import Image, ImageDraw, ImageFont
	from gtts import gTTS
except:
	print('Установка нужных пакетов')
	try:
		from pip import main as pipmain
	except:
		from pip._internal.main import main as pipmain
	pipmain(['install', 'requests'])
	pipmain(['install', 'pillow'])
	pipmain(['install', 'gTTS'])
	import requests, json, random, time, string, threading, textwrap
	from PIL import Image, ImageDraw, ImageFont
	
from func.get_updates import *
from func.friends import *
from func.status import *
from func.read_base import *
from func.me import *
from func.weather import *
from func.video import *
from func.audio import *
from func.tru import *
from func.online import *
from func.when import *
from func.infa import *
from func.who import *
from func.cities_func import *
from func.regular import *
from func.get_ans import *
from func.tell import *

try:
	with open('cities.json') as f:
		cities = json.load(f)
except:
	cities = False

with open('blacklist.txt') as f:
	f = f.read()
	blacklist = f.split('\n')[2:]
	black_mess = f.split('\n')[0]

def main(ac, TOKEN, STATUS, SLEEP, MARK, NAME, auto_friends, ls_user, group_name, base_name, group, commands, voice_bot):
	cities_users = {}
	disable_mentions = False
	regulars = ('id', 'first_name', 'last_name', 'about', 'bdate', 'city', 'count_messages', 'uptime')
	if not group:
		BotID = requests.get('https://api.vk.com/method/users.get', params = {'access_token': TOKEN, 'v': 5.21, 'fields': 'id'})
		BotID = json.loads(BotID.text)
		if 'error' in BotID:
			print(BotID)
		BotID = BotID['response'][0]['id']
	else:
		BotID = group
	count_message = 0
	base = read_base(base_name)
	key, server, ts = get_server(TOKEN, group)
	print(f'Аккаунт {ac} запущен')
	time_status = time.localtime()
	start_bot = time.time()
	if not group:
		status(STATUS, TOKEN, BotID, regulars, count_message, start_bot)
	if auto_friends and not group:
		friends(TOKEN, ac)
	while True:
		new_time_status = time.localtime()
		if ((time_status.tm_hour != new_time_status.tm_hour) or (time_status.tm_min != new_time_status.tm_min)) and not group:
			status(STATUS, TOKEN, BotID, regulars, count_message, start_bot)
			time_status = new_time_status
			if auto_friends:
				friends(TOKEN, ac)
		updates, key, server, ts = get_upd(TOKEN, key, server, ts)
		for i in updates:
			disable_mentions = False
			obr = True
			ls_ans = ls_user
			ans = []
			user = False
			attachments = 0
			message = 0
			tr = 0
			tr_group = False
			is_audio = False
			if not group:
				if i[0] == 4:
					if 'source_act' in i[-1]:
						if i[-1]['source_act'] == 'chat_kick_user':
							message = 'Выход из беседы'
						elif i[-1]['source_act'] in ('chat_invite_user', 'chat_invite_user_by_link', 'chat_create'):
							message = 'Вход в беседу'
						tr = 1
					if i[2] in (2, 3, 35):
						continue
					if 'from' in i[-1]:
						ls_ans = True
						if i[-1]['from'] == str(BotID):
							continue
						if 'source_mid' in i[-1]:
							user_id = i[-1]['source_mid']
						else:
							user_id = i[-1]['from']
						if int(user_id) > 0:
							while True:
								user = requests.get('https://api.vk.com/method/users.get', params = {'access_token': TOKEN, 'v': 5.21, 'fields': 'id', 'user_ids': user_id})
								user = json.loads(user.text)
								if 'error' in user:
									time.sleep(1)
									continue
								user = user['response'][0]
								break
					else:
						user_id = i[3]
					if not ans:
						if not message:
							message = i[-2]
						if NAME and ls_ans and not tr:
							if message[:len(NAME) +2].lower() == NAME + ', ':
								message = message[len(NAME)+2:]
							else:
								for black in blacklist:
									if black in message:
										ans = black_mess
										break
								else:
									if message.lower()[:4] == '/try' and user:
										attachments = tru(message, user, i, TOKEN)
									elif message.lower()[:3] == '/me' and user:
										attachments = me(message, user, TOKEN)
									else:
										continue
						if cities and (message.lower() == 'города' or user_id in cities_users):
							ans = cities_func(message, user_id, cities_users, cities)
						if message.lower()[:3] == 'кто':
							ans = who(i, TOKEN, group)
						if message.lower()[:4] == 'инфа':
							ans = infa()
						if message.lower()[:5] == 'когда':
							ans = when()
						if message.lower()[:6] == 'онлайн':
							ans, disable_mentions = online(i, message, TOKEN, disable_mentions, group)
						if message.lower()[:5] in ('музыка', 'аудио'):
							ans, attachments = audio(message, TOKEN)
						if message.lower()[:5] == 'видео':
							ans, attachments = video(message, TOKEN)
						if message.lower()[:6] == 'погода':
							ans = weather(message, user_id, TOKEN)
						if message.lower()[:5] == 'скажи':
							attachments = tell(message[6:], TOKEN, i[3], group, tr_group)
						if not ans and not attachments:
							for s in message:
								if s in string.ascii_letters:
									ans, attachments, is_audio = get_ans(message, base, commands, TOKEN, i[3], group, tr_group, voice_bot, user_id, count_message, start_bot, regulars)
									break
							if not ans:
								try:
									ans = str(round(eval(message), 3))
								except:
									ans, attachments, is_audio = get_ans(message, base, commands, TOKEN, i[3], group, tr_group, voice_bot, user_id, count_message, start_bot, regulars)
					if ans or attachments:
						if ans:
							for h in regulars:
								if h in ans.lower():
									ans = regular(ans, user_id, count_message, start_bot, TOKEN, regulars)
									break
						else:
							ans = ''
						if (user) and not('source_act' in i[-1]) and (group_name) and obr:
							ans = ans.split(' ')
							ans[0] = ans[0].lower()
							ans = user['first_name'] + ', ' + (" ").join(ans)
						if MARK:
							ans = '(' + MARK + ') ' + ans
						if SLEEP:
							sl = requests.post('https://api.vk.com/method/messages.setActivity', params = {'type': 'typing', 'peer_id':  i[3], 'access_token': TOKEN, 'v': 5.122})
							time.sleep(SLEEP)
						max = 0
						while True:
							if len(ans) > 500*(max+1):
								ans_ok = ans[500*max:500*(max+1)]
							else:
								ans_ok = ans[max*500:]
							paramss = {'access_token': TOKEN, 'peer_id': i[3], 'v': 5.87, 'message': ans_ok, 'disable_mentions': int(disable_mentions)}
							if attachments:
								paramss.update({'attachment':','.join(attachments)})
							a = requests.post('https://api.vk.com/method/messages.send', params = paramss)
							max += 1
							a = json.loads(a.text)
							if len(a) > 1:
								print(a)
							if len(ans) > 500 * max:
								continue
							break
						count_message += 1
						print('#'*10 + f' Аккаунт {ac} ' + '#'*10)
						print(f'Сообщение: {message}')
						print(f'Ответ: {ans}')
			else:
				if i['type'] == 'message_new':
					if 'action' in i['object']['message']:
						if i['object']['message']['action']['type'] == 'chat_kick_user':
							message = 'Выход из беседы'
						elif i['object']['message']['action']['type'] in ('chat_invite_user', 'chat_invite_user_by_link', 'chat_create'):
							message = 'Вход в беседу'
						tr = 1
					if i['object']['message']['peer_id'] > 2000000000:
						tr_group = True
						ls_ans = True
						if 'action' in i['object']['message']:
							user_id = i['object']['message']['action']['member_id']
						else:
							user_id = i['object']['message']['from_id']
						if int(user_id) > 0:
							while True:
								user = requests.get('https://api.vk.com/method/users.get', params = {'access_token': TOKEN, 'v': 5.21, 'fields': 'id', 'user_ids': user_id})
								user = json.loads(user.text)
								if 'error' in user:
									time.sleep(1)
									continue
								user = user['response'][0]
								break
					else:
						user_id = i['object']['message']['from_id']
					if not ans:
						if not message:
							if tr_group:
								message = i['object']['message']['text']
							else:
								message = i['object']['message']['text']
						if NAME and ls_ans and not tr:
							if message[:len(NAME) +2].lower() == NAME + ', ':
								message = message[len(NAME)+2:]
							else:
								for black in blacklist:
									if black in message:
										ans = black_mess
										break
								else:
									if message.lower()[:4] == '/try' and user:
										attachments = tru(message, user, i, TOKEN)
									elif message.lower()[:3] == '/me' and user:
										attachments = me(message, user, TOKEN)
									else:
										continue
						if cities and (message.lower() == 'города' or user_id in cities_users):
							ans = cities_func(message, user_id, cities_users, cities)
						if message.lower()[:3] == 'кто':
							ans = who(i, TOKEN, group)
						if message.lower()[:4] == 'инфа':
							ans = infa()
						if message.lower()[:5] == 'когда':
							ans = when()
						if message.lower()[:6] == 'онлайн':
							ans, disable_mentions = online(i, message, TOKEN, disable_mentions, group)
						if message.lower()[:6] == 'погода':
							ans = weather(message, user_id, TOKEN)
						if message.lower()[:5] == 'скажи':
							attachments = tell(message[6:], TOKEN, i['object']['message']['peer_id'], group, tr_group)
						if not ans and not attachments:
							for s in message:
								if s in string.ascii_letters:
									ans, attachments, is_audio = get_ans(message, base, commands, TOKEN, i['object']['message']['peer_id'], group, tr_group, voice_bot, user_id, count_message, start_bot, regulars)
									break
							if not ans:
								try:
									ans = str(round(eval(message), 3))
								except:
									ans, attachments, is_audio = get_ans(message, base, commands, TOKEN, i['object']['message']['peer_id'], group, tr_group, voice_bot, user_id, count_message, start_bot, regulars)
					if ans or attachments:
						if ans:
							for h in regulars:
								if h in ans.lower():
									ans = regular(ans, user_id, count_message, start_bot, TOKEN, regulars)
									break
						else:
							ans = ''
						if (user) and not tr and (group_name) and obr and tr_group:
							ans = ans.split(' ')
							ans[0] = ans[0].lower()
							ans = user['first_name'] + ', ' + (" ").join(ans)
						if MARK:
							ans = '(' + MARK + ') ' + ans
						if SLEEP:
							if is_audio:
								sl = requests.post('https://api.vk.com/method/messages.setActivity', params = {'type': 'audiomessage', 'peer_id':  i['object']['message']['peer_id'], 'access_token': TOKEN, 'v': 5.122})
							else:
								sl = requests.post('https://api.vk.com/method/messages.setActivity', params = {'type': 'typing', 'peer_id':  i['object']['message']['peer_id'], 'access_token': TOKEN, 'v': 5.122})
							time.sleep(SLEEP)
						max = 0
						while True:
							if len(ans) > 500*(max+1):
								ans_ok = ans[500*max:500*(max+1)]
							else:
								ans_ok = ans[max*500:]
							try:
								paramss = {'access_token': TOKEN, 'peer_id': i['object']['user_id'], 'v': 5.87, 'message': ans_ok, 'disable_mentions': int(disable_mentions)}
							except:
								paramss = {'access_token': TOKEN, 'peer_id': i['object']['message']['peer_id'], 'v': 5.87, 'message': ans_ok, 'disable_mentions': int(disable_mentions)}
							if attachments:
								paramss.update({'attachment':','.join(attachments)})
							a = requests.post('https://api.vk.com/method/messages.send', params = paramss)
							max += 1
							a = json.loads(a.text)
							if len(a) > 1:
								print(a)
							if len(ans) > 500 * max:
								continue
							break
						count_message += 1
						print('#'*10 + f' Аккаунт {ac} ' + '#'*10)
						print(f'Сообщение: {message}')
						print(f'Ответ: {ans}')
					
if __name__ == '__main__':
	ac = 1
	while True:
		try:
			with open(f'bot/accounts/{ac}/token.txt') as f:
				pass
		except:
			break
		try:
			with open(f'bot/accounts/{ac}/token.txt') as f:
				TOKEN = f.readline()
				if TOKEN[-1] == '\n':
					TOKEN = TOKEN[:-1]
					if TOKEN[0] == '-':
						group = TOKEN.split()[1]
						TOKEN = TOKEN.split()[0][1:]
					else:
						group = False
				a = f.readline()
				if a:
					NAME = a.lower()
					if NAME[-1] == '\n':
						NAME = NAME[:-1]
				else:
					NAME = False
				a = f.readline()
				if a:
					MARK = a
					if MARK[-1] == '\n':
						MARK = MARK[:-1]
				else:
					MARK = False
				a = f.readline()
				if a:
					SLEEP = float(a)
				else:
					SLEEP = False
				a = f.readline()
				if a:
					base_name = a
					if base_name[-1] == '\n':
						base_name = base_name[:-1]
			
			with open(f'bot/accounts/{ac}/settings.txt') as f:
				settings = f.readline().split()
				if '1' in settings:
					group_name = True
				else:
					group_name = False
				if '2' in settings:
					ls_user = True
				else:
					ls_user = False
				if '3' in settings:
					auto_friends = True
				else:
					auto_friends = False
				if '4' in settings:
					voice_bot = True
				else:
					voice_bot = False
			with open(f'bot/accounts/{ac}/commands.txt') as f:
				commands = []
				line = f.readline()
				while line:
					if line[-3] == '\\':
						line = line[:-3]
					line = line.split('\\')
					if len(line) >= 2:
						line1 = ''
						for i in range(1, len(line)):
							if line[i]:
								if line[i][0] == 'n':
									line1 += '\n' + line[i][1:]
								else:
									if i != 1:
										line += '\\'
									line1 += line[i]
						commands.append([line[0], line1])
					line = f.readline()
			with open(f'bot/accounts/{ac}/status.txt') as f:
				STATUS = f.read()
			threading.Thread(target=main, args=(ac, TOKEN, STATUS, SLEEP, MARK, NAME, auto_friends, ls_user, group_name, base_name, group, commands, voice_bot)).start()
		except Exception as err:
			print(f'Ошибка аккаунта {ac}', err)
		ac += 1