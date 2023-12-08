from time import sleep
from http.server import BaseHTTPRequestHandler, HTTPServer
import os


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # sleep before returning any requests, should contribute to 'latency.proxy'
        sleep(1.0)

        sleep_time = 2.0
        self.send_response(200)
        self.end_headers()
        self.wfile.write(f"starting sleep for {sleep_time} seconds\n".encode("utf-8"))

        # sleep after sending some bytes but before closing connection, should contribute to 'latency.kong'
        sleep(sleep_time)
        self.wfile.write(f"done".encode("utf-8"))


if __name__ == "__main__":
    domain, port = os.getenv("LISTEN_ADDRESS", "0.0.0.0:9090").split(":")

    server_address = (domain, int(port))
    with HTTPServer(server_address, Handler) as server:
        print(f"Listening on {domain}:{port}")
        while True:
            server.handle_request()
