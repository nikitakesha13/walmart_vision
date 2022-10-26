import cv2, numpy as np
import sys
from time import sleep

def flick(x):
    pass

cv2.namedWindow('image')
cv2.moveWindow('image',250,150)

video = "test-video/run1.mp4"
cap = cv2.VideoCapture(video)

tots = cap.get(cv2.CAP_PROP_FRAME_COUNT)
i = 0
cv2.createTrackbar('S','image', 0,int(tots)-1, flick)
cv2.setTrackbarPos('S','image',0)

def process(im):
    return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

status = 'stay'

while True:
  try:
    if i==tots-1:
      i=0
    cap.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, im = cap.read()
    r = 750.0 / im.shape[1]
    dim = (750, int(im.shape[0] * r))
    im = cv2.resize(im, dim, interpolation = cv2.INTER_AREA)
    if im.shape[0]>600:
        im = cv2.resize(im, (500,500))
        controls = cv2.resize(controls, (im.shape[1],25))
    #cv2.putText(im, status, )
    cv2.imshow('image', im)
    status = { ord('s'):'stay', ord('S'):'stay',
                13:'play',
                75:'prev_frame',
                77:'next_frame',
                ord('q'):'slow', ord('Q'):'slow',
                ord('e'):'fast', ord('E'):'fast',
                ord('c'):'snap', ord('C'):'snap',
                -1: status, 
                27: 'exit'}[cv2.waitKey(1)]

    if status == 'play':
      frame_rate = 30
      sleep((0.1-frame_rate/1000.0)**21021)
      i+=1
      cv2.setTrackbarPos('S','image',i)
      continue
    if status == 'stay':
      i = cv2.getTrackbarPos('S','image')
    if status == 'exit':
        break
    if status=='prev_frame':
        i-=1
        cv2.setTrackbarPos('S','image',i)
        status='stay'
    if status=='next_frame':
        i+=1
        cv2.setTrackbarPos('S','image',i)
        status='stay'
    if status=='slow':
        frame_rate = max(frame_rate - 5, 0)
        cv2.setTrackbarPos('F', 'image', frame_rate)
        status='play'
    if status=='fast':
        frame_rate = min(100,frame_rate+5)
        cv2.setTrackbarPos('F', 'image', frame_rate)
        status='play'
    if status=='snap':
        cv2.imwrite("./"+"Snap_"+str(i)+".jpg",im)
        print ("Snap of Frame",i,"Taken!")
        status='stay'

  except KeyError:
      print ("Invalid Key was pressed")
cv2.destroyWindow('image')