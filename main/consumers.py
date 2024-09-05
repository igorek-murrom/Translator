import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
import json


class VideoConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.send_task = None

    async def connect(self):
        await self.accept()
        self.send_task = asyncio.create_task(self.send_data())

    async def disconnect(self, close_code):
        self.send_task.cancel()

    async def send_data(self):
        while True:
            data = {
                'log': ['Hello, world!']
            }
            await self.send(text_data=json.dumps(data))
            await asyncio.sleep(0.02)  # Отправлять данные каждые 1 секунду
