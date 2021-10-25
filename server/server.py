import asyncio
from asyncio import Future
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional

import websockets

WEBSOCKET_PORT = 9999


class HTTPHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes("<h1>It works!</h1>", "utf-8"))

    def log_message(self, log_format: str, *args: any):
        return


class Server(object):

    @staticmethod
    async def __on_connect(websocket, path):
        print(f"New connection")
        async for message in websocket:
            print(f"Got message: {message}")
            await websocket.send(message)

    async def __start_websocket(self):
        async with websockets.serve(self.__on_connect, "localhost", WEBSOCKET_PORT):
            self.__stop = Future()
            await self.__stop

    def start(self):
        print(f"Started server on port {self.port}")
        http_server = HTTPServer(("localhost", self.port), HTTPHandler)
        threading.Thread(target=http_server.serve_forever).start()

        print(f"Hosting websocket endpoint on port {WEBSOCKET_PORT}")

        asyncio.run(self.__start_websocket())

    def stop(self):
        self.__stop.set_result(True)

    def __init__(self, port: int):
        self.port = port
        self.__stop: Optional[Future] = None
