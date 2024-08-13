import asyncio
import websockets
import cv2
import base64

class WebSocketServer:
    def __init__(self, port, host='localhost'):
        self.host = host
        self.port = port
        self.clients = set()
        self.server = None
        self.loop = asyncio.get_event_loop()

    async def handler(self, websocket, path):
        self.clients.add(websocket)
        try:
            async for message in websocket:
                pass
        finally:
            self.clients.remove(websocket)

    async def send_data(self, frame, delay):
        while True:
            await asyncio.sleep(delay)
            if self.clients:
                _, buffer = cv2.imencode('.jpg', frame)
                frame_base64 = base64.b64encode(buffer).decode('utf-8')
                await asyncio.wait([client.send(frame_base64) for client in self.clients])

    async def start(self):
        self.server = await websockets.serve(self.handler, self.host, self.port)
        await self.server.wait_closed()

    def stop(self):
        for task in asyncio.all_tasks(self.loop):
            task.cancel()
        self.loop.stop()



class API:
    def __init__(self):
        self.ws = [WebSocketServer(x) for x in range(8100, 8105)]

    def init_video(self, index):
        asyncio.create_task(self.ws[index].start)

    def send_video(self, index, frame, delay=0.01):
        asyncio.get_event_loop().run_until_complete(self.ws[index].send_data(frame, delay))

    def stop_video(self, index):
        self.ws[index].stop()
