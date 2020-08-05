
def read_base(name):
	with open('bot/base/' + name) as f:
		base = []
		line = f.readline()
		while line:
			if line[-3] == '\\':
				line = line[:-3]
			line = line.split('\\')
			if len(line) >= 2:
				line1 = ''
				for i in range(1, len(line)):
					if line[i]:
						if line[i][0] == 'n':
							line1 += '\n' + line[i][1:]
						else:
							if i != 1:
								line += '\\'
							line1 += line[i]
				base.append([line[0], line1])
			line = f.readline()
	return base