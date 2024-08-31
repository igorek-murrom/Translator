Это проект, который упрощает отладку и загрузку скриптов для робота

ОШИБКИ ПОЛЬЗОВАТЕЛЬСКИХ СКРИПТОВ НЕ ОБРАБАТЫВЮТСЯ, АМИНЬ.

Он поддерживает передачу до 5 видео одновременно (формата opencv) и логирование, ручной запуск и остановку скрипта, автозапуск скрипта при включении сервера.

Для загрузки кода необходимо нажать на кнопку 'Upload Code' и выбрать все нужные файлы.

Для того, чтобы работали кнопки старта, остановки и автостарт, необходимо нажать на кнопку 'Edit command' и прописать нужную команду, которая будет отрабатывать при нажатии кнопки старт и при автостарте (Это команда сохранится при выключении сервера).
Например для запуска python скрипта с именем 'main.py' необходимо прописать комманду (обратите внимане на путь, все ваши файлы будут находиться по пути 'sub/project' в иерархии сервера):
```text
python3 sub/project/main.py
```

Чтобы работал автостарт, необходимо загрузить файл с именем 'autostart.txt' с содержимым:
```text
True
```

Зависимости:
django, websockets, opencv-python

Для запуска необходимо:
1) узнать локальный айпи-адресс в сети (используйте ifconfig или ip a)
2) найденный айпи вписываем в файл по пути djangoProject/settings.py в переменную MAIN_HOST

Команда для запуска (вместо ip укажите найденный айпи-адресс):
```text
python3 manage.py runserver ip:8000 --noreload
```

Для удобной работы создайте файл (или вставьте в главный скрипт) с кодом:
``` python
from django.conf import settings
import asyncio
import websockets
import base64
import cv2
import threading
import json


def fix_image(image):
    _, buffer = cv2.imencode('.jpg', image)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    return encoded_image


class ImageWebSocketServer:
    def __init__(self, host='localhost', port=8100):
        self.host = host
        self.port = port
        self.images = {}
        self.log = {}
        self.clients = set()
        self.log_cnt = 0

    async def register(self, websocket):
        self.clients.add(websocket)

    async def unregister(self, websocket):
        self.clients.remove(websocket)

    async def send_image(self, websocket, path):
        await self.register(websocket)
        try:
            await websocket.wait_closed()
        finally:
            await self.unregister(websocket)

    def set_image(self, image, number):
        if 0 < number < 10:
            self.images[number] = fix_image(image)

    def set_log(self, log):
        self.log[self.log_cnt] = str(log)
        self.log_cnt += 1

    async def broadcast(self):
        while True:
            message = {}
            if self.log:
                message['log'] = self.log
                self.log = {}
                self.log_cnt = 0
            if self.images:
                message['images'] = self.images
                self.images = {}

            if message and self.clients:
                json_message = json.dumps(message)
                tasks = [asyncio.create_task(client.send(json_message)) for client in self.clients]
                # FIXME
                try:
                    await asyncio.gather(*tasks)
                except:
                    print("error")

            await asyncio.sleep(0.001)

    def start_server(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(self.send_image, self.host, self.port)
        loop.run_until_complete(start_server)
        loop.create_task(self.broadcast())
        print(f"Server started at ws://{self.host}:{self.port}")
        loop.run_forever()

class Robot:
    def __init__(self, host=settings.MAIN_HOST):
        self.server = ImageWebSocketServer(host)
        server_thread = threading.Thread(target=self.server.start_server)
        server_thread.start()

    def show(self, image, channel: int) -> None:
        self.server.set_image(image, channel)

    def log(self, msg):
        self.server.set_log(msg)

```