import random

def cities_func(message, user_id, cities_users, cities):
	if message.lower() == 'закончить игру':
		del cities_users[user_id]
		ans =  'Игра окончена'
	else:
		if message.lower() == 'города':
			cities_users[user_id] = []
			city = random.choice(cities)
			ans =  f'Ну давай поиграем в города, я начну:\n{city}'
			cities_users[user_id].append(city)
		else:
			simv = cities_users[user_id][-1][-1]
			if simv in 'ыьъ':
				simv = cities_users[user_id][-1][-2]
			if message in cities:
				if message in cities_users[user_id]:
					ans = 'Этот город уже был'
				elif message[0].lower() != simv:
					ans = f'Не та буква, сейчас тебе нужно назвать город на букву: {simv.upper()}'
				else:
					simv_mess = message[-1]
					if simv_mess in 'ыьъ':
						simv_mess = message[-2]
					cities_users[user_id].append(message)
					for h in cities:
						if (h not in cities_users[user_id]) and (h[0].lower() == simv_mess):
							ans = h
							cities_users[user_id].append(ans)
							break
					else:
						ans = 'Я не знаю, что ответить\nТы победил'
						del cities_users[user_id]
			else:
				ans = f'Я не знаю такого города. \nТебе нужно назвать город на букву {simv.upper()} \nЧтобы закончить игру, напиши: "Закончить игру"'
	return ans