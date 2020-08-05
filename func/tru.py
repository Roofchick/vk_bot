import requests, json, random, textwrap
from PIL import Image, ImageDraw, ImageFont

def tru(message, user, i, TOKEN):
	rand = random.randint(0,1)
	message = message[5:]
	if len(message) > 13:
		if message[13] in ('@', '*'):
			id = message[3:12]
			user = requests.get('https://api.vk.com/method/users.get', params = {'access_token': TOKEN, 'v': 5.21, 'fields': 'id', 'user_ids': id})
			user = json.loads(user.text)['response'][0]
			messs = 2
			for i in message:
				if i == ']':
					message = message[messs:]
					break
				messs += 1
	ans = user['first_name'] + ' ' + user['last_name'] + ' ' + message
	if rand:
		result = 'Удачно'
	else:
		result = 'Неудачно'
	astr = ans
	para = textwrap.wrap(astr, width=15)

	MAX_W, MAX_H = 200, 200
	if result == 'Удачно':
		color = (18,255,1,255)
	else:
		color = (255,0,17,255)
	im = Image.new('RGB', (MAX_W, MAX_H), color)
	draw = ImageDraw.Draw(im)
	font = ImageFont.truetype(
    'arial.ttf', 18)

	current_h, pad = 50, 10
	for line in para:
	    w, h = draw.textsize(line, font=font)
	    draw.text(((MAX_W - w) / 2, current_h), line, font=font, fill=(3, 8, 12))
	    current_h += h + pad
	im.save('test.png')
	a = requests.post('https://api.vk.com/method/photos.getMessagesUploadServer', params = {'access_token': TOKEN, 'v':5.98})
	a = requests.post(json.loads(a.text)['response']['upload_url'], files = {'photo': open('test.png', 'rb')})
	a = json.loads(a.text)
	a =requests.post('https://api.vk.com/method/photos.saveMessagesPhoto', params = {'access_token': TOKEN, 'v':5.98, 'photo': a['photo'], 'server': a['server'], 'hash': a['hash']})
	a = json.loads(a.text)['response'][0]
	return [f'photo{a["owner_id"]}_{a["id"]}',]