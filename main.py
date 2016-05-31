# Создать приложение здесь http://vk.com/editapp?act=create
# Выбрать Standalone-приложение

# для получения токена нужно посылать запрос с браузера

# https://oauth.vk.com/authorize?client_id=5461499&display=page&callback&scope=audio&response_type=token&v=5.52
# 5461499 это номер приложения, ругистрируется здесь http://vk.com/editapp?act=create

# подтверждаем права для приложения, значение из access_token вставлять для авторизации сессии
# там както хитро сделано у них что GET запросом через requests не получается токен выдрать

import vk
import requests
import shutil
import os


PATH_TO_SAVE_FILES = 'D:\\vkmusic'


def to_correct_name(name):
    name = name.replace('*', '_').replace('|', '').replace('\\', '_')\
               .replace(':', '').replace('"', '`').replace('<', '')\
               .replace('>', '').replace('?', '').replace('/', '')
    return name


session = vk.Session(access_token='ce815d3f9ff620943c2f2e6f77248289cade0964c5ba36f6ef850d6553e415f1e65599d68ae6f2a1251ca')
api = vk.API(session)
audio_objects = api.audio.get()
#audio_objects = api.audio.get(count=30)

for obj in audio_objects:
    url = obj['url'].split('?')[0]
    title = obj['title']
    name = '%s.mp3' % to_correct_name(title)
    downloaded_files = [f for f in os.listdir(PATH_TO_SAVE_FILES) if os.path.isfile(os.path.join(PATH_TO_SAVE_FILES, f))]

    if name not in downloaded_files:
        print('-->    %s' % name)
        resp = requests.get(url, stream=True)
        if resp.status_code == 200:
            path = os.path.join(PATH_TO_SAVE_FILES, name)
            with open(path, 'wb') as f:
                resp.raw.decode_content = True
                shutil.copyfileobj(resp.raw, f)

print('DONE!')