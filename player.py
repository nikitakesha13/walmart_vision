import cv2, numpy as np
import sys
from time import sleep

thickness = 5
lineColor = (0, 255, 0)
dotColor = (0, 255, 0)
radius = 15

def flick():
    pass

def readTxtFile(filename):
    f = open(filename, "r")
    content = f.readlines()
    allPoints = []
    for line in content:
        allPoints.append([float(v) for v in line.split()])
    return allPoints
    
myPoints = readTxtFile("points.txt")

def drawLine(image, x1, y1, x2, y2):
    cv2.line(image, (x1,y1), (x2,y2), lineColor, thickness)
    cv2.circle(image, (x1,y1), radius, dotColor, thickness)
    cv2.circle(image, (x2,y2), radius, dotColor, thickness)

video = "test-video/wyatt.mp4"
cap = cv2.VideoCapture(video)

tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
i = 0

def process(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

status = 'play'

frameWidth = int(cap.get(3))
frameHeight = int(cap.get(4))
size = (frameWidth, frameHeight)

result = cv2.VideoWriter("test-video-out/test.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 30, size)

while True:
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, im = cap.read()
    for p in range(1, len(myPoints[i])-3,4):
        drawLine(im, int(myPoints[i][p]), int(myPoints[i][p+1]), int(myPoints[i][p+2]), int(myPoints[i][p+3]))
    result.write(im)
    print ("frame", i)

    if i == tots-1:
        break

    if status == 'play':
      i+=1
      continue
