import requests, json, time

def friends(TOKEN, ac):
	followers = requests.get('https://api.vk.com/method/users.getFollowers', params = {'access_token': TOKEN, 'v': 5.21})
	followers = json.loads(followers.text)['response']['items']
	for i in followers:
		while True:
			user = requests.get('https://api.vk.com/method/users.get', params = {'access_token': TOKEN, 'v': 5.21, 'fields': 'id', 'user_ids': i})
			user = json.loads(user.text)
			if 'error' in user:
				time.sleep(1)
				continue
			user = user['response'][0]
			break
		if 'deactivated' in user:
			requests.post('https://api.vk.com/method/account.ban', params = {'access_token': TOKEN, 'v': 5.21, 'owner_id': user['id']})
			requests.post('https://api.vk.com/method/account.unban', params = {'access_token': TOKEN, 'v': 5.21, 'owner_id': user['id']})
			continue
		requests.post('https://api.vk.com/method/friends.add', params = {'access_token': TOKEN, 'v': 5.21, 'user_id': user['id']})
		print('#'*10 + f' Аккаунт {ac} ' + '#'*10)
		print(f'Принята заявка от {user["first_name"]} {user["last_name"]}')