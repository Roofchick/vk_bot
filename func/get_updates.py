import requests, json

def get_server(TOKEN, group):
	while True:
		try:
			if group:
				a = 'groups'
			else:
				a = 'messages'
			paramss = {'lp_version': 3, 'v': 5.65 , 'access_token': TOKEN}
			if group:
				paramss.update({'group_id': group})
			a = requests.get('https://api.vk.com/method/' + a + '.getLongPollServer', params = paramss)
			a = json.loads(a.text)['response']
			key = a['key']
			server = a['server']
			ts = a['ts']
			if server[:8] == 'https://':
				server = server[8:]
			return key, server, ts
			break
		except:
			continue
	

def get_upd(TOKEN, key, server, ts):
	while True:
		try:
			b = requests.get(f'https://{server}', params = {'act': 'a_check', 'key': key, 'ts': ts, 'wait': 40, 'versions': 3, 'mode': 10})
			upd = json.loads(b.text)
			if 'failed' in upd:
				print(upd)
				if upd['failed'] == 1:
					ts = upd['ts']
					return get_upd(TOKEN, key, server, ts)
				elif upd['failed'] in (2,3):
					key, server, ts = get_server(TOKEN)
					return get_upd(TOKEN, key, server, ts)
			ts = upd['ts']
			return upd['updates'], key, server, ts
			break
		except:
			continue