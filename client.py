import base64
import sys
import json
import urllib2

imagePath=sys.argv[1]

with open(imagePath, "rb") as imageFile:
    encodedImage = base64.b64encode(imageFile.read())

jsonData = {}
jsonData['imageBase64'] = encodedImage
jsonRequest = json.dumps(jsonData)

httpRequest = urllib2.Request('http://localhost:8000')
httpRequest.add_header('Content-Type', 'application/json')

httpResponse = urllib2.urlopen(httpRequest, jsonRequest)

print httpResponse.read()
