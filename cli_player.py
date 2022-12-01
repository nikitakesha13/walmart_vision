
import cv2, numpy as np
import sys
from time import sleep


class CLI_Player:
    def __init__(self, _path):
        self.path = _path
        self.thickness = 5
        self.lineColor = (0, 255, 0)
        self.dotColor = (0, 255, 0)
        self.radius = 15
        self.cap = cv2.VideoCapture(self.path + "/result.avi")

    def drawLine(self, image, x1, y1, x2, y2):
        cv2.circle(image, (x1,y1), self.radius, self.dotColor, self.thickness)
        cv2.circle(image, (x2,y2), self.radius, self.dotColor, self.thickness)

    def flick(self, x):
        pass

    def cli_play(self):

        cv2.namedWindow('image')
        cv2.moveWindow('image',250,150)
        cv2.namedWindow('controls')
        cv2.moveWindow('controls',250,50)

        controls = np.zeros((50,750),np.uint8)
        cv2.putText(controls, "W/w: Play, S/s: Stay, A/a: Prev, D/d: Next, E/e: Fast, Q/q: Slow, Esc: Exit", (40,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)

        video = "test-video/wyatt.mp4"
        cap = cv2.VideoCapture(video)

        tots = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        i = 0
        cv2.createTrackbar('S','image', 0,int(tots)-1, self.flick)
        cv2.setTrackbarPos('S','image',0)

        cv2.createTrackbar('F','image', 1, 100, self.flick)
        frame_rate = 30
        cv2.setTrackbarPos('F','image',frame_rate)

        status = 'stay'

        while True:
            cv2.imshow("controls",controls)
            try:
                if i==tots-1:
                    i=0
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, im = self.cap.read()
                cv2.imshow('image', im)
                status = { ord('s'):'stay', ord('S'):'stay',
                            ord('w'):'play', ord('W'):'play',
                            ord('a'):'prev_frame', ord('A'):'prev_frame',
                            ord('d'):'next_frame', ord('D'):'next_frame',
                            ord('q'):'slow', ord('Q'):'slow',
                            ord('e'):'fast', ord('E'):'fast',
                            ord('c'):'snap', ord('C'):'snap',
                            -1: status, 
                            27: 'exit'}[cv2.waitKey(10)]

                if status == 'play':
                    frame_rate = cv2.getTrackbarPos('F','image')
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
                    print (")Snap of Frame",i,"Taken!")
                    status='stay'

            except KeyError:
                print ("Invalid Key was pressed")

        cv2.destroyWindow('image')