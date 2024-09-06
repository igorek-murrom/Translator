import json
import cv2
import base64
import fcntl


def fix_image(image):
    _, buffer = cv2.imencode('.jpg', image)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    return encoded_image


class Robot:
    def __init__(self):
        self.keys = []
        self.images = {}
        self.log = {}
        self.log_cnt = 0

    def msg(self, msg):
        self.log[self.log_cnt] = str(msg)
        self.log_cnt += 1

    def show(self, img, num):
        if 0 < num < 6:
            self.images[num] = fix_image(img)

    def send(self):
        message = {}
        if self.log:
            message['log'] = self.log
            self.log = {}
            self.log_cnt = 0
        if self.images:
            message['images'] = self.images
            self.images = {}

        if message:
            with open("/mnt/ramdisk/transitIN.txt", 'w') as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                f.write(json.dumps(message))
                fcntl.flock(f, fcntl.LOCK_UN)

    def read_key(self):
        try:
            with open('/mnt/ramdisk/transitOUT.txt', 'r') as f:
                fcntl.flock(f, fcntl.LOCK_SH)
                self.keys = json.loads(f.read())
                fcntl.flock(f, fcntl.LOCK_UN)
        except:
            pass
        return self.keys


robot = Robot()
cnt = 0
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    robot.show(frame, 1)
    robot.show(cv2.flip(frame, 0), 2)
    robot.show(cv2.flip(frame, 1), 3)

    robot.msg(cnt)
    cnt += 1
    robot.send()

    print(robot.read_key())