from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
from SocketServer import ThreadingMixIn
import threading
import json
import base64
import os
from io import BytesIO
# image resize
from PIL import Image

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200) # ok
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        # recievedImage
        requestData = json.loads(self.rfile.read(content_length).encode('utf8'))
        decodedImage = base64.b64decode(requestData['imageBase64'])

        # resizing imageFile... 10% of original size
        imgfile = BytesIO(decodedImage)
        resizedBuffered = BytesIO()
        with Image.open(imgfile) as image:
            image = image.resize((int(0.1 * image.size[0]), int(0.1 * image.size[1])), Image.ANTIALIAS)
            image.save(resizedBuffered, format="JPEG")

        # print "send to client"
        encodedImage = base64.b64encode(resizedBuffered.getvalue())

        self._set_headers()
        jsonData = {}
        jsonData['resizedImage'] = encodedImage
        jsonResponse = json.dumps(jsonData)
        self.wfile.write(jsonResponse)

def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

# class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
#     """Handle requests in a separate thread."""

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
# if __name__ == '__main__':
#     server = ThreadedHTTPServer(('localhost', 8000), S)
#     print 'Starting server, use <Ctrl-C> to stop'
#     server.serve_forever()
