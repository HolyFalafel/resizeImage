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

imagePath = "temp.jpg"
videoPath = sys.argv[1] # path of video file
N = int(sys.argv[2]) # num of frames
M = int(sys.argv[3]) # time between frames

# opening video
vidcap = cv2.VideoCapture(videoPath)
print "opening ", videoPath
success,image = vidcap.read()
# with open(imagePath, "w") as frameFile:
#     frameFile.write(image)

for frame_number in range(0, N-1):
    # getting the frame in time delta M
    frame = getVideoFrame(frame_number * M, vidcap)

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

    # receiving image
    httpResponse = urllib2.urlopen(httpRequest, jsonRequest)

    # print httpResponse.read()
    content_length = int(self.headers['Content-Length'])
    # recievedImage
    requestData = json.loads(self.rfile.read(content_length).encode('utf8'))
    decodedImage = base64.b64decode(requestData['resizedImage'])
    recievedImageFilename = 'frame%d.jpg' % frame_number+1
    testFile = open(recievedImageFilename, 'w')
    testFile.write(decodedImage)
    testFile.close()
