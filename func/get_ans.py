import random, time
from func.tell import *
from func.regular import *
from func.append_attach import *
from func.randoms import *

def get_ans(message, base, commands, TOKEN, peer_id, group, tr_group, voice_bot, user_id, count_message, start_bot, regulars):
	max_g = 0
	ans = []
	g = 0
	for f in commands:
		if f[0].lower() == message.lower():
			ans = f[1]
			break
	else:
		for f in base:
			if f and len(f) > 1:
				s1, s2 = message.lower(), f[0].lower()
				max = len(s2)
				if len(s1) > len(s2):
					s1, s2 = s2, s1
					max = len(s2)
				p = 0
				for i in range(len(s1)):
					if s1[i] == s2[i]:
						p += 1
					g = int(p/max*100)
				if g > max_g:
					ans = [f[1],]
					max_g = g
				if g == max_g:
					ans.append(f[1])
	if ans:
		ans = random.choice(ans)
		if '@[' in ans:
			ans = randoms(ans)
		if 'https://vk.com/' in ans:
			return append_attach(ans)
		if (ans[0] == '{' and ans[-1] == '}') or voice_bot:
			for h in regulars:
				if h in ans.lower():
					ans = regular(ans, user_id, count_message, start_bot, TOKEN, regulars)
					break
			return '', tell(ans, TOKEN, peer_id, group, tr_group), True
		else:
			return ans, '', False