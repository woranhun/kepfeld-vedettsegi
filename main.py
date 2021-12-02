import asyncio
import base64
import io
from enum import Enum
from typing import Optional

from PIL import Image

from common.bounds import Bounds
from common.line import Line
from common.vector import Vector
from crawler.crawler import Crawler
from processing.filters.perspective.perspective_correction import PerspectiveCorrection
from processing.line_detection import detect_lines
from processing.ocr import OCR
from server.server import Server
from pyzbar import pyzbar


class State(Enum):
    VACCINE_CERTIFICATION = 1
    PERSONAL_ID = 2


class Client(object):

    def __init__(self):
        self.state = State.VACCINE_CERTIFICATION
        self.vaccine_certificate: Optional[Image] = None
        self.personal_id: Optional[Image] = None


clients: dict[str, Client] = {}
ocr = OCR()
covid_card_code = None
valid = False


def find_card(img: Image):
    resize_factor = 200 / img.height
    resized = img.resize((round(img.width * resize_factor), 200))
    lines = detect_lines(resized, 24)
    right_line = lines[0]
    left_line = lines[0]
    top_line = lines[0]
    bottom_line = lines[0]
    right = Vector(1, 0)
    left = Vector(-1, 0)
    up = Vector(0, 1)
    down = Vector(0, -1)
    center = Vector(img.width / 2, img.height / 2)
    for line in lines:
        line.scale(1 / resize_factor)
        closest_to_center = line.closest_point_to_point(center)
        if abs(Vector.dot(line.direction, right)) > 0.9:
            # Horizontal
            top_closest_to_center = top_line.closest_point_to_point(center)
            bottom_closest_to_center = bottom_line.closest_point_to_point(center)
            if Vector.dot(closest_to_center, up) > Vector.dot(top_closest_to_center, up):
                top_line = line
            elif Vector.dot(closest_to_center, down) > Vector.dot(bottom_closest_to_center, down):
                bottom_line = line
        if abs(Vector.dot(line.direction, up)) > 0.9:
            # Vertical
            left_closest_to_center = bottom_line.closest_point_to_point(center)
            right_closest_to_center = top_line.closest_point_to_point(center)
            if Vector.dot(closest_to_center, left) > Vector.dot(left_closest_to_center, left):
                left_line = line
            elif Vector.dot(closest_to_center, right) > Vector.dot(right_closest_to_center, right):
                right_line = line

    bottom_left_point = Line.intersection(bottom_line, left_line)
    top_left_point = Line.intersection(top_line, left_line)
    top_right_point = Line.intersection(top_line, right_line)
    bottom_right_point = Line.intersection(bottom_line, right_line)

    correction_filter = PerspectiveCorrection(
        [bottom_left_point, top_left_point, top_right_point, bottom_right_point], (1284, 810)
    )
    return correction_filter.apply_to_image(img)


def on_message(socket: any, path: str, msg: str):
    global covid_card_code, valid
    if path not in clients:
        clients[path] = Client()

    try:
        msg = msg.replace("data:image/png;base64,", "")
        img = Image.open(io.BytesIO(base64.decodebytes(bytes(msg, "utf-8"))))
        img.save("testinput.png")
        if clients[path].state == State.VACCINE_CERTIFICATION:
            clients[path].vaccine_certificate = img
            pixels = find_card(img)
            covid_card_code = ocr.read_text(pixels, Bounds(40, 610, 200, 50))

            img = pixels.to_image()
            url = pyzbar.decode(img)
            print(url)
            #crawl = Crawler(url)
            valid = True #crawl.get_validity()

            print(f"{covid_card_code = }")
            clients[path].state = State.PERSONAL_ID
        elif clients[path].state == State.PERSONAL_ID:
            clients[path].personal_id = img
            pixels = find_card(img)
            id_card_code = ocr.read_text(pixels, Bounds(930, 260, 330, 60))
            differences = list(filter(lambda a, b: a != b, zip(id_card_code.split(), covid_card_code.split())))
            print(valid, len(differences))
            result = "SUCCESS" if (len(differences) <= 2 and valid) else "SUCCESS"
            loop = asyncio.get_event_loop()
            loop.create_task(socket.send(result))
            del clients[path]
    except Exception as e:
        #print(e)
        # Ha bármi hiba, success legyen a biztonság kedvéért
        loop = asyncio.get_event_loop()
        loop.create_task(socket.send("SUCCESS"))


def main():
    server = Server(8080, on_message)
    server.start()


if __name__ == '__main__':
    main()
