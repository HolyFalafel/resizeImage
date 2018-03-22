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

temp_dir = "./temp/"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
imagePath = temp_dir+"temp.jpg"

def getVideoFrame(time, cap):
    cap.set(cv2.CAP_PROP_POS_MSEC, time * 1000)  # Go to the time * 1 sec. position
    ret, frame = cap.read() # retrieves the frame at the specified second
    return frame

def handleVideoInstance(curr_instance, videoPath):
    print "instance number ", curr_instance+1
    # creating output directory
    out_directory = '/tmp/vid-instance'+str(curr_instance+1)+'/'
    if not os.path.exists(out_directory):
        os.makedirs(out_directory)

    # reading video instance
    vidcap = cv2.VideoCapture(videoPath)
    print "opening ", videoPath
    success,frame = vidcap.read()

    frame_number = 1

    while success:
        # getting the frame in time delta M
        # frame = getVideoFrame(frame_number * M, vidcap)

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
        print "receiving from server"
        httpResponse = urllib2.urlopen(httpRequest, jsonRequest)

        # receivedImage
        responseData = json.loads(httpResponse.read().encode('utf8'))
        decodedImage = base64.b64decode(responseData['resizedImage'])
        recievedImageFilename = out_directory+'Frame'+format(frame_number+1, '05d') +'.jpg'
        print "saving frame number ", frame_number+1, " as ", recievedImageFilename
        testFile = open(recievedImageFilename, 'w')
        testFile.write(decodedImage)
        testFile.close()

        # reading next frame
        success,frame = vidcap.read()
        frame_number +=1

try:
    videoPath = sys.argv[1] # path of video file
    N = int(sys.argv[2]) # num of frames
    M = int(sys.argv[3]) # time between frames
except:
    print "Error reading params, call structure is: client.py videoPath, N, M"
    sys.exit(1)

# opening video
vidcap = cv2.VideoCapture(videoPath)
print "opening ", videoPath
success,image = vidcap.read()

if not success:
    print "Error reading video file"
    sys.exit(1)

# running the N instances within time difference M
for curr_instance in range(0, N):
    # handleVideoInstance(curr_instance, videoPath)
    thread.start_new_thread(handleVideoInstance, (curr_instance, videoPath))
    time.sleep(M)

# removing temp directory
shutil.rmtree(temp_dir, ignore_errors=True)
