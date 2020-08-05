import requests, json, textwrap
from PIL import Image, ImageDraw, ImageFont

def me(message, user, TOKEN):
	ans = user['first_name'] + ' ' + user['last_name'] + message[3:]
	astr = ans
	para = textwrap.wrap(astr, width=15)

	MAX_W, MAX_H = 200, 200
	im = Image.new('RGB', (MAX_W, MAX_H), (0, 0, 0, 0))
	draw = ImageDraw.Draw(im)
	font = ImageFont.truetype(
    'arial.ttf', 18)

	current_h, pad = 50, 10
	for line in para:
	    w, h = draw.textsize(line, font=font)
	    draw.text(((MAX_W - w) / 2, current_h), line, font=font)
	    current_h += h + pad
	im.save('test.png')
	a = requests.post('https://api.vk.com/method/photos.getMessagesUploadServer', params = {'access_token': TOKEN, 'v':5.98})
	a = requests.post(json.loads(a.text)['response']['upload_url'], files = {'photo': open('test.png', 'rb')})
	a = json.loads(a.text)
	a =requests.post('https://api.vk.com/method/photos.saveMessagesPhoto', params = {'access_token': TOKEN, 'v':5.98, 'photo': a['photo'], 'server': a['server'], 'hash': a['hash']})
	a = json.loads(a.text)['response'][0]
	return [f'photo{a["owner_id"]}_{a["id"]}',]