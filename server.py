from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import json
import base64
import os
# image resize
from PIL import Image
# from resizeimage import resizeimage

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
        recievedImageFilename = 'recievedImage.jpg'
        with open(recievedImageFilename, 'w') as testFile:
            testFile.write(decodedImage)
            testFile.close()

        resizedImageFilename = 'resizedImage.jpg'
        # resizing imageFile... 10% of original size
        with open(recievedImageFilename,'r') as f:
            with Image.open(f) as image:
                image = image.resize((int(0.1 * image.size[0]), int(0.1 * image.size[1])), Image.ANTIALIAS)
                image.save(resizedImageFilename)
            f.close()

        # print "send to client"
        with open(resizedImageFilename, "rb") as imageFile:
            encodedImage = base64.b64encode(imageFile.read())
        self._set_headers()
        jsonData = {}
        jsonData['resizedImage'] = encodedImage
        jsonResponse = json.dumps(jsonData)
        self.wfile.write(jsonResponse)

        # deleting files
        # try:
        #     os.remove(recievedImageFilename)
        #     os.remove(resizedImageFilename)
        # except:
        #     print "error removing temp files"

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
