import requests, json

def audio(message, TOKEN):
	mess = message[6:]
	r = requests.get('https://api.vk.com/method/audio.search', params = {'access_token': TOKEN, 'q': mess, 'AutoComplete': 1, 'sort': 2, 'count': 10, 'v': 5.44})
	audio = json.loads(r.text)['response']['items']
	attachment = []
	for i in audio:
		attachment.append('audio' + str(i['owner_id']) + '_' + str(i['id']))
	return f'Аудио по запросу:', attachment