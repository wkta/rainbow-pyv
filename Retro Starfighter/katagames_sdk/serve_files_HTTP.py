import http.server
# from http.server import HTTPServer, BaseHTTPRequestHandler
import socketserver
# import sys


PORT = 8000


def do_serve():
    Handler = http.server.SimpleHTTPRequestHandler

    Handler.extensions_map={
        '.manifest': 'text/cache-manifest',
        '.html': 'text/html',
        '.txt': 'text/plain',
        '.png': 'image/png',
        '.jpg': 'image/jpg',
        '.svg': 'image/svg+xml',
        '.css': 'text/css',
        '.js': 'application/x-javascript',
        '.json': 'application/json',
        '.xml': 'application/xml',
        '.wasm': 'application/wasm',
        '': 'application/octet-stream', # Default
    }

    httpd = socketserver.TCPServer(("", PORT), Handler)

    print("serving at port", PORT)
    print("serving at http://127.0.0.1:{}/".format(PORT))
    httpd.serve_forever()


if __name__ == '__main__':
    do_serve()
