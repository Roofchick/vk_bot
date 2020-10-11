try:
    import requests, json, random, time, string, threading, textwrap
    from PIL import Image, ImageDraw, ImageFont
    from gtts import gTTS
except:
    print('Установка нужных пакетов')
    try:
        from pip import main as pipmain
    except:
        from pip._internal.main import main as pipmain
    pipmain(['install', 'requests'])
    pipmain(['install', 'pillow'])
    pipmain(['install', 'gTTS'])
    import requests, json, random, time, string, threading, textwrap
    from PIL import Image, ImageDraw, ImageFont

from func.get_updates import *
from func.friends import *
from func.status import *
from func.read_base import *
from func.me import *
from func.weather import *
from func.video import *
from func.audio import *
from func.tru import *
from func.online import *
from func.when import *
from func.infa import *
from func.who import *
from func.cities_func import *
from func.regular import *
from func.get_ans import *
from func.tell import *
from func.account_start import *

try:
    with open('cities.json') as f:
        cities = json.load(f)
except:
    cities = False

with open('blacklist.txt') as f:
    f = f.read()
    blacklist = f.split('\n')[2:]
    black_mess = f.split('\n')[0]


def main(ac, TOKEN, STATUS, SLEEP, MARK, NAME, auto_friends, ls_user, group_name, base_name, group, commands, voice_bot,
         reply):
    cities_users = {}
    disable_mentions = False
    regulars = ('id', 'first_name', 'last_name', 'about', 'bdate', 'city', 'count_messages', 'uptime')
    if not group:
        BotID = requests.get('https://api.vk.com/method/users.get',
                             params={'access_token': TOKEN, 'v': 5.21, 'fields': 'id'})
        BotID = json.loads(BotID.text)
        if 'error' in BotID:
            print(BotID)
        BotID = BotID['response'][0]['id']
    else:
        BotID = group
    count_message = 0
    base = read_base(base_name)
    key, server, ts = get_server(TOKEN, group)
    print(f'Аккаунт {ac} запущен')
    time_status = time.localtime()
    start_bot = time.time()
    if not group:
        status(STATUS, TOKEN, BotID, regulars, count_message, start_bot)
    if auto_friends and not group:
        friends(TOKEN, ac)
    while True:
        new_time_status = time.localtime()
        if ((time_status.tm_hour != new_time_status.tm_hour) or (
                time_status.tm_min != new_time_status.tm_min)) and not group:
            status(STATUS, TOKEN, BotID, regulars, count_message, start_bot)
            time_status = new_time_status
            if auto_friends:
                friends(TOKEN, ac)
        updates, key, server, ts = get_upd(TOKEN, key, server, ts, group)
        for i in updates:
            disable_mentions = False
            obr = True
            ls_ans = ls_user
            ans = []
            user = False
            attachments = 0
            message = 0
            tr = 0
            tr_group = False
            is_audio = False
            if not group:
                if i[0] == 4:
                    if 'source_act' in i[-1]:
                        if i[-1]['source_act'] == 'chat_kick_user':
                            message = 'Выход из беседы'
                        elif i[-1]['source_act'] in ('chat_invite_user', 'chat_invite_user_by_link', 'chat_create'):
                            message = 'Вход в беседу'
                        tr = 1
                    if 'from' in i[-1]:
                        ls_ans = True
                        if i[-1]['from'] == str(BotID):
                            continue
                        if 'source_mid' in i[-1]:
                            user_id = i[-1]['source_mid']
                        else:
                            user_id = i[-1]['from']
                        if int(user_id) > 0:
                            while True:
                                user = requests.get('https://api.vk.com/method/users.get',
                                                    params={'access_token': TOKEN, 'v': 5.21, 'fields': 'id',
                                                            'user_ids': user_id})
                                user = json.loads(user.text)
                                if 'error' in user:
                                    time.sleep(1)
                                    continue
                                user = user['response'][0]
                                break
                    else:
                        a = requests.get("https://api.vk.com/method/messages.getById",
                                         params={"access_token": TOKEN, "v": 5.121, "message_ids": i[1],
                                                 "preview_length": 1})
                        a = json.loads(a.text)["response"]["items"][0]["from_id"]
                        if a == BotID:
                            continue
                        user_id = i[3]
                    if not ans:
                        if not message:
                            message = i[-2]
                        if NAME and ls_ans and not tr:
                            if message[:len(NAME) + 2].lower() == NAME + ', ':
                                message = message[len(NAME) + 2:]
                            else:
                                for black in blacklist:
                                    if black in message:
                                        ans = black_mess
                                        break
                                else:
                                    if 'reply' in i[-1]:
                                        conv_mess_id = json.loads(i[-1]['reply'])
                                        conv_mess_id = conv_mess_id['conversation_message_id']
                                        a = requests.get("https://api.vk.com/method/messages.getByConversationMessageId",
                                                            params={"access_token": TOKEN, "v": 5.121, "peer_id": i[3],
                                                            "conversation_message_ids": conv_mess_id})
                                        a = json.loads(a.text)["response"]["items"][0]["from_id"]
                                        if a != BotID:
                                            continue
                                    else:
                                        if message.lower()[:4] == '/try' and user:
                                            attachments = tru(message, user, i, TOKEN)
                                        elif message.lower()[:3] == '/me' and user:
                                            attachments = me(message, user, TOKEN)
                                        else:
                                            continue
                        if cities and (message.lower() == 'города' or user_id in cities_users):
                            ans = cities_func(message, user_id, cities_users, cities)
                        if message.lower()[:3] == 'кто':
                            ans = who(i, TOKEN, group)
                        if message.lower()[:4] == 'инфа':
                            ans = infa()
                        if message.lower()[:5] == 'когда':
                            ans = when()
                        if message.lower()[:6] == 'онлайн':
                            ans, disable_mentions = online(i, message, TOKEN, disable_mentions, group)
                        if message.lower()[:5] in ('музыка', 'аудио'):
                            ans, attachments = audio(message, TOKEN)
                        if message.lower()[:5] == 'видео':
                            ans, attachments = video(message, TOKEN)
                        if message.lower()[:6] == 'погода':
                            ans = weather(message, user_id, TOKEN)
                        if message.lower()[:5] == 'скажи':
                            attachments = tell(message[6:], TOKEN, i[3], group, tr_group)
                            is_audio = True
                        if not ans and not attachments:
                            for s in message:
                                if s in string.ascii_letters:
                                    ans, attachments, is_audio = get_ans(message, base, commands, TOKEN, i[3], group,
                                                                         tr_group, voice_bot, user_id, count_message,
                                                                         start_bot, regulars)
                                    break
                            if not ans:
                                try:
                                    ans = str(round(eval(message), 3))
                                except:
                                    ans, attachments, is_audio = get_ans(message, base, commands, TOKEN, i[3], group,
                                                                         tr_group, voice_bot, user_id, count_message,
                                                                         start_bot, regulars)
                    if ans or attachments:
                        if ans:
                            for h in regulars:
                                if h in ans.lower():
                                    ans = regular(ans, user_id, count_message, start_bot, TOKEN, regulars)
                                    break
                        else:
                            ans = ''
                        if (user) and not ('source_act' in i[-1]) and (group_name) and obr:
                            ans = ans.split(' ')
                            ans[0] = ans[0].lower()
                            ans = user['first_name'] + ', ' + (" ").join(ans)
                        if MARK:
                            ans = '(' + MARK + ') ' + ans
                        if SLEEP:
                            if is_audio:
                                sl = requests.post('https://api.vk.com/method/messages.setActivity',
                                                   params={'type': 'audiomessage', 'peer_id': i[3],
                                                           'access_token': TOKEN, 'v': 5.122})
                            else:
                                sl = requests.post('https://api.vk.com/method/messages.setActivity',
                                                   params={'type': 'typing', 'peer_id': i[3], 'access_token': TOKEN,
                                                           'v': 5.122})
                            time.sleep(SLEEP)
                        max = 0
                        while True:
                            if len(ans) > 500 * (max + 1):
                                ans_ok = ans[500 * max:500 * (max + 1)]
                            else:
                                ans_ok = ans[max * 500:]
                            paramss = {'access_token': TOKEN, 'peer_id': i[3], 'v': 5.122, 'message': ans_ok,
                                       'disable_mentions': int(disable_mentions),
                                       'random_id': random.randint(1, 1000000)}
                            if attachments:
                                paramss.update({'attachment': ','.join(attachments)})
                            if reply and ls_ans:
                                paramss.update({'reply_to': i[1]})
                            a = requests.post('https://api.vk.com/method/messages.send', params=paramss)
                            print(a.text)
                            max += 1
                            a = json.loads(a.text)
                            if len(a) > 1:
                                print(a)
                            if len(ans) > 500 * max:
                                continue
                            break
                        count_message += 1
                        print('#' * 10 + f' Аккаунт {ac} ' + '#' * 10)
                        print(f'Сообщение: {message}')
                        print(f'Ответ: {ans}')
            else:
                if i['type'] == 'message_new':
                    if 'action' in i['object']['message']:
                        if i['object']['message']['action']['type'] == 'chat_kick_user':
                            message = 'Выход из беседы'
                        elif i['object']['message']['action']['type'] in (
                        'chat_invite_user', 'chat_invite_user_by_link', 'chat_create'):
                            message = 'Вход в беседу'
                        tr = 1
                    if i['object']['message']['peer_id'] > 2000000000:
                        tr_group = True
                        ls_ans = True
                        if 'action' in i['object']['message']:
                            user_id = i['object']['message']['action']['member_id']
                        else:
                            user_id = i['object']['message']['from_id']
                        if int(user_id) > 0:
                            while True:
                                user = requests.get('https://api.vk.com/method/users.get',
                                                    params={'access_token': TOKEN, 'v': 5.21, 'fields': 'id',
                                                            'user_ids': user_id})
                                user = json.loads(user.text)
                                if 'error' in user:
                                    time.sleep(1)
                                    continue
                                user = user['response'][0]
                                break
                    else:
                        user_id = i['object']['message']['from_id']
                    if not ans:
                        if not message:
                            if tr_group:
                                message = i['object']['message']['text']
                            else:
                                message = i['object']['message']['text']
                        if NAME and ls_ans and not tr:
                            if message[:len(NAME) + 2].lower() == NAME + ', ':
                                message = message[len(NAME) + 2:]
                            else:
                                for black in blacklist:
                                    if black in message:
                                        ans = black_mess
                                        break
                                else:
                                    print(i)
                                    if 'reply_message' in i['object']['message']:
                                        reply_mess_id = i['object']['message']['reply_message']['from_id']
                                        if str(reply_mess_id)[1:] != BotID:
                                            print(type(BotID), type(str(reply_mess_id)[1:]), BotID, str(reply_mess_id)[1:])
                                            continue
                                    else:
                                        if message.lower()[:4] == '/try' and user:
                                            attachments = tru(message, user, i, TOKEN)
                                        elif message.lower()[:3] == '/me' and user:
                                            attachments = me(message, user, TOKEN)
                                        else:
                                            continue
                        if cities and (message.lower() == 'города' or user_id in cities_users):
                            ans = cities_func(message, user_id, cities_users, cities)
                        if message.lower()[:3] == 'кто':
                            ans = who(i, TOKEN, group)
                        if message.lower()[:4] == 'инфа':
                            ans = infa()
                        if message.lower()[:5] == 'когда':
                            ans = when()
                        if message.lower()[:6] == 'онлайн':
                            ans, disable_mentions = online(i, message, TOKEN, disable_mentions, group)
                        if message.lower()[:6] == 'погода':
                            ans = weather(message, user_id, TOKEN)
                        if message.lower()[:5] == 'скажи':
                            attachments = tell(message[6:], TOKEN, i['object']['message']['peer_id'], group, tr_group)
                            is_audio = True
                        if not ans and not attachments:
                            for s in message:
                                if s in string.ascii_letters:
                                    ans, attachments, is_audio = get_ans(message, base, commands, TOKEN,
                                                                         i['object']['message']['peer_id'], group,
                                                                         tr_group, voice_bot, user_id, count_message,
                                                                         start_bot, regulars)
                                    break
                            if not ans:
                                try:
                                    ans = str(round(eval(message), 3))
                                except:
                                    ans, attachments, is_audio = get_ans(message, base, commands, TOKEN,
                                                                         i['object']['message']['peer_id'], group,
                                                                         tr_group, voice_bot, user_id, count_message,
                                                                         start_bot, regulars)
                    if ans or attachments:
                        if ans:
                            for h in regulars:
                                if h in ans.lower():
                                    ans = regular(ans, user_id, count_message, start_bot, TOKEN, regulars)
                                    break
                        else:
                            ans = ''
                        if (user) and not tr and (group_name) and obr and tr_group:
                            ans = ans.split(' ')
                            ans[0] = ans[0].lower()
                            ans = user['first_name'] + ', ' + (" ").join(ans)
                        if MARK:
                            ans = '(' + MARK + ') ' + ans
                        if SLEEP:
                            if is_audio:
                                sl = requests.post('https://api.vk.com/method/messages.setActivity',
                                                   params={'type': 'audiomessage',
                                                           'peer_id': i['object']['message']['peer_id'],
                                                           'access_token': TOKEN, 'v': 5.122})
                            else:
                                sl = requests.post('https://api.vk.com/method/messages.setActivity',
                                                   params={'type': 'typing',
                                                           'peer_id': i['object']['message']['peer_id'],
                                                           'access_token': TOKEN, 'v': 5.122})
                            time.sleep(SLEEP)
                        max = 0
                        while True:
                            if len(ans) > 500 * (max + 1):
                                ans_ok = ans[500 * max:500 * (max + 1)]
                            else:
                                ans_ok = ans[max * 500:]
                            try:
                                paramss = {'access_token': TOKEN, 'peer_id': i['object']['user_id'], 'v': 5.92,
                                           'message': ans_ok, 'disable_mentions': int(disable_mentions),
                                           'random_id': random.randint(1, 11000000)}
                            except:
                                paramss = {'access_token': TOKEN, 'peer_id': i['object']['message']['peer_id'],
                                           'v': 5.92, 'message': ans_ok, 'disable_mentions': int(disable_mentions),
                                           'random_id': random.randint(1, 11000000)}
                            if attachments:
                                paramss.update({'attachment': ','.join(attachments)})
                            '''
							if reply:
								print(i)
								paramss.update({'reply_to': i['object']['message']['conversation_message_id']})
							'''
                            a = requests.post('https://api.vk.com/method/messages.send', params=paramss)
                            max += 1
                            a = json.loads(a.text)
                            if len(a) > 1:
                                print(a)
                            if len(ans) > 500 * max:
                                continue
                            break
                        count_message += 1
                        print('#' * 10 + f' Аккаунт {ac} ' + '#' * 10)
                        print(f'Сообщение: {message}')
                        print(f'Ответ: {ans}')


if __name__ == '__main__':
    start()
