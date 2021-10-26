import asyncio
import socketserver
from asyncio import Future
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional, Callable

import websockets

WEBSOCKET_PORT = 9999
REDIRECTS = {
    "/": "/index.html",
}
CONTENT_TYPES = {
    "js": "text/javascript",
    "css": "text/css",
    "html": "text/html",
    "htm": "text/html",
    "ico": "image/x-icon"
}


class HTTPHandler(BaseHTTPRequestHandler):

    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer):
        file_404 = open("server/client/404/404.html", "rb")
        self.content_404 = file_404.read()
        super().__init__(request, client_address, server)

    def __send_404(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(self.content_404)

    def do_GET(self):
        path = self.path
        if path in REDIRECTS:
            path = REDIRECTS[path]

        extension = path.split(".")[-1]
        if extension not in CONTENT_TYPES:
            self.__send_404()
            return
        content_type = CONTENT_TYPES[extension] or "text/plain"

        try:
            file = open(f"server/client{path}", "rb")

            content = file.read()
        except FileNotFoundError:
            self.__send_404()
            return

        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, log_format: str, *args: any):
        return


class Server(object):

    async def __on_connect(self, websocket, path):
        print(f"New connection")
        async for message in websocket:
            self.message_listener(websocket, path, message)

    async def __start_websocket(self):
        async with websockets.serve(self.__on_connect, "192.168.1.139", WEBSOCKET_PORT):
            self.__stop = Future()
            await self.__stop

    def start(self):
        print(f"Started server on port {self.port}")
        http_server = HTTPServer(("192.168.1.139", self.port), HTTPHandler)
        threading.Thread(target=http_server.serve_forever).start()

        print(f"Hosting websocket endpoint on port {WEBSOCKET_PORT}")

        asyncio.run(self.__start_websocket())

    def stop(self):
        self.__stop.set_result(True)

    def __init__(self, port: int, message_listener: Callable[[any, str, str], None]):
        self.port = port
        self.message_listener = message_listener
        self.__stop: Optional[Future] = None
