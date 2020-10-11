import threading

from main import main

def start():
    ac = 1
    while True:
        try:
            with open(f'bot/accounts/{ac}/token.txt', encoding="utf8") as f:
                pass
        except:
            break
        try:
            with open(f'bot/accounts/{ac}/token.txt', encoding="utf8") as f:
                TOKEN = f.readline()
                if TOKEN[-1] == '\n':
                    TOKEN = TOKEN[:-1]
                    if TOKEN[0] == '-':
                        group = TOKEN.split()[1]
                        TOKEN = TOKEN.split()[0][1:]
                    else:
                        group = False
                a = f.readline()
                if a:
                    NAME = a.lower()
                    if NAME[-1] == '\n':
                        NAME = NAME[:-1]
                else:
                    NAME = False
                a = f.readline()
                if a:
                    MARK = a
                    if MARK[-1] == '\n':
                        MARK = MARK[:-1]
                else:
                    MARK = False
                a = f.readline()
                if a:
                    SLEEP = float(a)
                else:
                    SLEEP = False
                a = f.readline()
                if a:
                    base_name = a
                    if base_name[-1] == '\n':
                        base_name = base_name[:-1]

            with open(f'bot/accounts/{ac}/settings.txt', encoding="utf8") as f:
                settings = f.readline().split()
                if '1' in settings:
                    group_name = True
                else:
                    group_name = False
                if '2' in settings:
                    ls_user = True
                else:
                    ls_user = False
                if '3' in settings:
                    auto_friends = True
                else:
                    auto_friends = False
                if '4' in settings:
                    voice_bot = True
                else:
                    voice_bot = False
                if '5' in settings:
                    reply = True
                else:
                    reply = False
            with open(f'bot/accounts/{ac}/commands.txt', encoding="utf8") as f:
                commands = []
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
                        commands.append([line[0], line1])
                    line = f.readline()
            with open(f'bot/accounts/{ac}/status.txt', encoding="utf8") as f:
                STATUS = f.read()
            threading.Thread(target=main, args=(
                ac, TOKEN, STATUS, SLEEP, MARK, NAME, auto_friends, ls_user, group_name, base_name, group, commands,
                voice_bot, reply)).start()
        except Exception as err:
            print(f'Ошибка аккаунта {ac}', err)
        ac += 1