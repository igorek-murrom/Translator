import cv2
import base64
import asyncio
import websockets

async def send_video(websocket, path):
    # Открываем камеру (0 - это индекс камеры по умолчанию)
    cap = cv2.VideoCapture(0)

    try:
        while cap.isOpened():
            # Читаем кадр с камеры
            ret, frame = cap.read()
            if not ret:
                break

            # Кодируем кадр в формат JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')

            # Отправляем кадр клиенту
            await websocket.send(frame_base64)

            # Задержка для ограничения частоты кадров
            await asyncio.sleep(0.01)
    finally:
        cap.release()

async def main():
    async with websockets.serve(send_video, "localhost", 8101):
        await asyncio.Future()  # Бесконечное ожидание

if __name__ == "__main__":
    asyncio.run(main())
#
#
# from robot_api import API
#
# robot = API.API()
#
# import cv2
#
# cap = cv2.VideoCapture(0)
# robot.init_video(0)
#
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break
#     robot.send_video(0, frame)
#
# robot.stop_video()
