import base64
import sys
import json
import urllib2

# video libraries
import cv2

def getVideoFrame(time, cap):
    cap.set(cv2.CAP_PROP_POS_MSEC, time * 1000)  # Go to the time * 1 sec. position
    ret, frame = cap.read() # retrieves the frame at the specified second
    return frame

imagePath = sys.argv[1]
videoPath = sys.argv[2]

# opening video
vidcap = cv2.VideoCapture(videoPath)
print "opening ", videoPath
success,image = vidcap.read()
# with open(imagePath, "w") as frameFile:
#     frameFile.write(image)

# going to 1 second frame
frame = getVideoFrame(1, vidcap)
# print frame
count = 1
cv2.imwrite(imagePath, frame)     # save frame as JPEG file

# read image - to send to server
print "send to server"
with open(imagePath, "rb") as imageFile:
    encodedImage = base64.b64encode(imageFile.read())

# sending image
jsonData = {}
jsonData['imageBase64'] = encodedImage
jsonRequest = json.dumps(jsonData)

httpRequest = urllib2.Request('http://localhost:8000')
httpRequest.add_header('Content-Type', 'application/json')

httpResponse = urllib2.urlopen(httpRequest, jsonRequest)

print httpResponse.read()
