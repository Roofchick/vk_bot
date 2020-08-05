import requests, json, time

def regular(mess, user, count_message, start_bot, TOKEN, regulars):
	ans = ''
	regular = ''
	f = False
	for i in mess:
		if f:
			if i == '%':
				if regular.lower() in regulars:
					if regular.lower() == 'count_messages':
						ans += str(count_message)
					elif regular.lower() == 'uptime':
						new_sec = int(time.time() - start_bot)
						h = new_sec // 60 // 60
						m = new_sec // 60 - h * 60
						s = new_sec - m * 60 - h * 60 * 60
						ans += f'{h} час. {m} мин. {s} сек.'
					else:
						while True:
							r = requests.get('https://api.vk.com/method/users.get', params = {'access_token': TOKEN, 'v': 5.21, 'fields': regular.lower(), 'user_ids': user})
							r = json.loads(r.text)
							if 'error' in r:
								time.sleep(1)
								continue
							if regular.lower() == 'city':
								r = r['response'][0][regular.lower()]['title']
							else:
								r = r['response'][0][regular.lower()]
							ans += str(r)
							break
				else:
					ans += '%' + regular + '%'
				regular = ''
				f = False
			else:
				regular += i
		else:
			if i == '%':
				f = True
				continue
			ans += i
	if regular != '':
		ans += '%' + regular
	return ans