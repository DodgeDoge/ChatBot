import random

import requests
import vk_api
from Config import *

def write_msg(user_id, text):
    vk_bot.method('messages.send', {'user_id': user_id, 'message': text, 'random_id': random.randint(0, 1000)})

vk_bot = vk_api.VkApi(token=ACCESS_TOKEN)
long_poll = vk_bot.method('messages.getLongPollServer', {'need_pts': 1, 'lp_version': 3})
server, key, ts = long_poll['server'], long_poll['key'], long_poll['ts']
#print(server)
#print(key)
#print(ts)
print('готов к работе')
# + str(long_poll))

while True:
    new_ts = vk_bot.method('messages.getLongPollServer', {'need_pts': 1, 'lp_version': 3})
    ts = new_ts['ts']
    long_poll = requests.get('https://{server}?act={act}&key={key}&ts={ts}&wait=500'.format(server=server,
                                                                                            act='a_check',
                                                                                            key=key,
                                                                                            ts=ts)).json()
    update = long_poll['updates']
    if update[0][0] == 4 and  update[0][3] != 321056236 and update[0][6] == 'привет' or 'Привет':
        user_id = update[0][3]
        user_name = vk_bot.method('users.get', {'user_ids': user_id})
        write_msg(user_id, 'привет, ' + (user_name[0]['first_name'])) #сообщение пользователю