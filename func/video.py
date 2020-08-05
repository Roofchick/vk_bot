import requests, json

def video(message, TOKEN):
	mess = message[6:]
	r = requests.get('https://api.vk.com/method/video.search', params = {'access_token': TOKEN, 'q': mess, 'sort': 2, 'count': 10, 'v': 5.44})
	video = json.loads(r.text)['response']['items']
	attachment = []
	for i in video:
		attachment.append('video' + str(i['owner_id']) + '_' + str(i['id']))
	return f'Видео по запросу:', attachment