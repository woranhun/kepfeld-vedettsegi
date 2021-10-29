import asyncio
import base64
import colorsys
import io
from enum import Enum
from typing import Optional

from PIL import Image

from common.line import Line
from common.vector import Vector
from debug_tools import draw_line_on_image
from processing.line_detection import detect_lines
from server.server import Server


class State(Enum):
    VACCINE_CERTIFICATION = 1
    PERSONAL_ID = 2


class Client(object):

    def __init__(self):
        self.state = State.VACCINE_CERTIFICATION
        self.vaccine_certificate: Optional[Image] = None
        self.personal_id: Optional[Image] = None


clients: dict[str, Client] = {}


def on_message(socket: any, path: str, msg: str):
    if path not in clients:
        clients[path] = Client()

    msg = msg.replace("data:image/png;base64,", "")
    img = Image.open(io.BytesIO(base64.decodebytes(bytes(msg, "utf-8"))))
    if clients[path].state == State.VACCINE_CERTIFICATION:
        clients[path].vaccine_certificate = img
        print("Got image")
        resized = img.resize((round(200 / img.height * img.width), 200))
        lines = detect_lines(resized, 8)
        for i, line in enumerate(lines):
            draw_line_on_image(resized, line, (255 - i * 30, i * 30, 0))

        resized.show()
        clients[path].state = State.PERSONAL_ID
    elif clients[path].state == State.PERSONAL_ID:
        clients[path].personal_id = img
        # TODO: Do checks
        loop = asyncio.get_event_loop()
        loop.create_task(socket.send("SUCCESS"))
        del clients[path]


def main():
    server = Server(8080, on_message)
    server.start()


if __name__ == '__main__':
    main()
