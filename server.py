from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import base64

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        requestData = json.loads(self.rfile.read(content_length).encode('utf8'))
        decodedImage = base64.b64decode(requestData['imageBase64'])
        testFile = open('recievedImage.jpg', 'w')
        testFile.write(decodedImage)
        testFile.close()


        self._set_headers()
        jsonData = {}
        jsonData['status'] = 'ok'
        jsonResponse = json.dumps(jsonData)
        self.wfile.write(jsonResponse)

def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
