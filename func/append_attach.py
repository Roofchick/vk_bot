
def append_attach(mess):
	ans = ''
	regular = ''
	attach = []
	f = False
	for i in mess:
		if f:
			if i == '*':
				if regular[15:20] in ('photo', 'video', 'audio') or regular[15:19] in ('poll', 'wall') or regular[15:18] == 'doc' or regular[15:21] == 'market':
					attach.append(regular[15:])
				else:
					ans += '*' + regular + '*'
				regular = ''
				f = False
			else:
				regular += i
		else:
			if i == '*':
				f = True
				continue
			ans += i
	if regular != '':
		ans += '*' + regular
	return ans, attach, False