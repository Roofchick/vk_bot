import random

def when():
	return f'Я думаю через {random.randint(1, 1000)} {random.choice(["дней", "часов", "минут", "секунд", "лет", "месяцев"])}'