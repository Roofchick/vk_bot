import requests, json, time

def online(i, message, TOKEN, disable_mentions, group):
	if group:
		params = {'access_token': TOKEN, 'v':5.85, 'peer_id': i['object']['message']['peer_id']}
	else:
		params = {'access_token': TOKEN, 'v':5.85, 'peer_id': i[3]}
	members = requests.get('https://api.vk.com/method/messages.getConversationMembers', params = params)
	members = json.loads(members.text)
	online = []
	disable_mentions = True
	for f in members['response']['profiles']:
		if 'is_online' not in f['online_info']:
			continue
		if f['online_info']['is_online']:
			online.append(f)
	ans = f'Сейчас онлайн {len(online)} человек:\n'
	for f in online:
		ans += f'• [id{f["id"]}|{f["first_name"]} {f["last_name"]}]'
		if 'app_id' in f['online_info'] and not group:
			while True:
				app = requests.get('https://api.vk.com/method/apps.get', params = {'access_token': TOKEN, 'v':5.21, 'app_id': f['online_info']['app_id']})
				app = json.loads(app.text)
				if 'error' in app:
					time.sleep(1)
					continue
				app = app['response']['title']
				break
			ans += ' через ' + app + '\n'
		else:
			if not group:
				ans +=  ' через Web-версию\n'
			else:
				ans += '\n'
	return ans, disable_mentions