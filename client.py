import base64
import sys
import json
import urllib2
import os
import shutil

# video library
import cv2

# mulithreading and time
import thread
import time

tempDir = "./temp/"
if not os.path.exists(tempDir):
    os.makedirs(tempDir)
imagePath = tempDir+"temp.jpg"

def handleVideoInstance(currInstanceNum, videoPath):
    start = time.time()
    print "starting instance number", currInstanceNum+1
    # creating output directory
    outDirectory = '/tmp/vid-instance'+str(currInstanceNum+1)+'/'
    if not os.path.exists(outDirectory):
        os.makedirs(outDirectory)

    # reading video instance
    vidcap = cv2.VideoCapture(videoPath)
    # print "opening ", videoPath
    success,frame = vidcap.read()

    frameNumber = 1

    while success:
        cv2.imwrite(imagePath, frame)     # save frame as JPEG file

        # read image - to send to server
        # print "send to server"
        with open(imagePath, "rb") as imageFile:
            encodedImage = base64.b64encode(imageFile.read())

        # sending image
        jsonData = {}
        jsonData['imageBase64'] = encodedImage
        jsonRequest = json.dumps(jsonData)

        httpRequest = urllib2.Request('http://localhost:8000')
        httpRequest.add_header('Content-Type', 'application/json')

        # receiving image
        # print "receiving from server"
        httpResponse = urllib2.urlopen(httpRequest, jsonRequest)

        # receivedImage
        responseData = json.loads(httpResponse.read().encode('utf8'))
        decodedImage = base64.b64decode(responseData['resizedImage'])
        recievedImageFilename = outDirectory+'Frame'+format(frameNumber, '05d') +'.jpg'
        # print "saving frame number ", frameNumber+1, " as ", recievedImageFilename
        testFile = open(recievedImageFilename, 'w')
        testFile.write(decodedImage)
        testFile.close()

        # reading next frame
        success,frame = vidcap.read()
        frameNumber +=1
    end = time.time()
    totTime = end - start
    print "video", currInstanceNum+1, "converted.", frameNumber-1, "frames total"
    print "files location:", outDirectory
    print "instance number", currInstanceNum+1, "took", totTime, "seconds"
    print "average frame rate", (frameNumber-1)/totTime, "fps"


try:
    videoPath = sys.argv[1] # path of video file
    N = int(sys.argv[2]) # num of frames
    M = int(sys.argv[3]) # time between frames
except:
    print "Error reading params, call structure is: client.py videoPath, N, M"
    sys.exit(1)

# opening video
vidcap = cv2.VideoCapture(videoPath)
print "opening video", videoPath
success,image = vidcap.read()

if not success:
    print "Error reading video file"
    sys.exit(1)

# running the N instances within time difference M
for currInstanceNum in range(0, N):
    thread.start_new_thread(handleVideoInstance, (currInstanceNum, videoPath))
    # waiting M seconds for the next instance
    time.sleep(M)

time.sleep(100000000)
# removing temp directory
shutil.rmtree(tempDir, ignore_errors=True)
