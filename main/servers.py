import asyncio
import websockets
import json
import fcntl
from django.conf import settings

connected_clients = set()


async def echo(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            await websocket.send(message)
    finally:
        connected_clients.remove(websocket)


async def send_periodic_data():
    old_msg = ""
    while True:
        if connected_clients:
            serialized_data = json.dumps(settings.DATA)
            if settings.DATA == old_msg:
                # settings.DATA = {}
                continue
            tasks = []
            disconnected_clients = set()
            for client in connected_clients:
                try:
                    tasks.append(client.send(serialized_data))
                except websockets.exceptions.ConnectionClosedOK:
                    print(f"Client {client.remote_address} closed the connection.")
                    disconnected_clients.add(client)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    disconnected_clients.add(client)
            connected_clients.difference_update(disconnected_clients)
            await asyncio.gather(*tasks)
            old_msg = settings.DATA

        await asyncio.sleep(0.02)


def start_websocket():
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_server = websockets.serve(echo, settings.MAIN_HOST, 8100)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.create_task(send_periodic_data())
    loop.run_forever()


def read():
    data = ""
    with open("/mnt/ramdisk/transitIN.txt", 'r') as f:
        fcntl.flock(f, fcntl.LOCK_SH)
        data = f.read()
        fcntl.flock(f, fcntl.LOCK_UN)
    return data


def start_socket():
    while True:
        if settings.PROCESS is not None:
            try:
                settings.DATA = json.loads(read())
            except:
                pass