from gtts import gTTS
import requests, json, string

def tell(message, TOKEN, peer_id, group, tr_group):
	if message[0] in string.ascii_letters:
		lang = 'en'
	else:
		lang = 'ru'
	myobj = gTTS(text=message, lang=lang, slow=False)
	myobj.save("tell.mp3")
	a = requests.post('https://api.vk.com/method/docs.getMessagesUploadServer', params = {'access_token': TOKEN, 'v':5.98, 'type': 'audio_message', 'peer_id': peer_id})
	a = requests.post(json.loads(a.text)['response']['upload_url'], files = {'file': open('tell.mp3', 'rb')})
	a = json.loads(a.text)
	a =requests.post('https://api.vk.com/method/docs.save', params = {'access_token': TOKEN, 'v':5.98, 'file': a['file']})
	a = json.loads(a.text)['response']['audio_message']
	print([f'doc{a["owner_id"]}_{a["id"]}',])
	return [f'doc{a["owner_id"]}_{a["id"]}',]