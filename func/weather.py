import requests, json

def weather(message, user_id, TOKEN):
	if message[7:]:
		city = message[7:]
	else:
		try:
			city = json.loads(requests.get('https://api.vk.com/method/users.get', params = {'access_token': TOKEN, 'v': 5.21, 'fields': 'city', 'user_ids': user_id}).text)['response'][0]['city']['title']
		except:
			return "Город не указан"
			
	r = requests.get('https://api.openweathermap.org/data/2.5/weather', params={'q': city, 'appid': '1a76779da9308a046daa80b2780216e9'})
	r = json.loads(r.text)
	if r['cod'] == '404':
		return 'Город не найден'
	j = int(r['main']['temp']) - 273
	country = r['sys']['country']
	city_name = r['name']
	return f'Погода в {country} {city_name}: {j}°'