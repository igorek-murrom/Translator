import socket
import asyncio
import time

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
                try:
                    await asyncio.gather(*tasks)
                except Exception as e:
                    print(f"Error broadcasting message: {e}")

            await asyncio.sleep(0.001)

    async def start_server(self):
        async with websockets.serve(self.send_image, self.host, self.port):
            print(f"Server started at ws://{self.host}:{self.port}")
            await self.broadcast()


class Robot:
    def __init__(self):
        self.server = ImageWebSocketServer(socket.gethostbyname(socket.gethostname()))
        self.key_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.key_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.key_socket.bind(('', 65432))

        self.keys = []

        thread = threading.Thread(target=self.run_server)
        thread.start()

    def show(self, image, channel: int) -> None:
        self.server.set_image(image, channel)

    def log(self, msg) -> None:
        self.server.set_log(msg)

    def read_keys(self):
        return self.keys

    def run_server(self):
        asyncio.run(self.start_server())

    async def start_server(self):
        server_task = asyncio.create_task(self.server.start_server())
        key_task = asyncio.create_task(self.task_read())
        await asyncio.gather(server_task, key_task)

    async def task_read(self):
        print("Key server started")
        while True:
            data, _ = await asyncio.get_event_loop().run_in_executor(None, self.key_socket.recvfrom, 1024)
            self.keys = json.loads(data.decode('utf-8'))


robot = Robot()
cnt = 0
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret: continue
    robot.show(frame, 1)
    robot.show(cv2.flip(frame, 0), 2)
    robot.show(cv2.flip(frame, 1), 3)

    robot.log(cnt)
    cnt += 1
    print(robot.read_keys())