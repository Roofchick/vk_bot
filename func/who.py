import requests, json, random

def who(i, TOKEN, group):
	if group:
		params = {'access_token': TOKEN, 'v':5.85, 'peer_id': i['object']['message']['peer_id'], 'group_id': group}
	else:
		params = {'access_token': TOKEN, 'v':5.85, 'peer_id': i[3]}
	members = requests.get('https://api.vk.com/method/messages.getConversationMembers', params = params)
	try:
		members = json.loads(members.text)['response']['profiles']
		member = random.choice(members)
		return f'Я думаю, что это [id{member["id"]}|{member["first_name"]}]'
	except:
		return 'Не могу выполнить данную команду, т.к. не являюсь администратором беседы'