import cv2
from form_analysis import Analysis
from misc import *
from report_gen import Report

msgDesc = ["Elbow", "Back lean", "Back bending", "Knee bending"]

class DrawVideo:
    def __init__(self, name, arr):
        self.video = name 
        self.cap = cv2.VideoCapture(self.video + "form_analysis.avi")
        self.tots = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.myPoints = arr

        self.frameWidth = int(self.cap.get(3))
        self.frameHeight = int(self.cap.get(4))
        self.size = (self.frameWidth, self.frameHeight)

        self.result = cv2.VideoWriter(self.video + "result.avi", cv2.VideoWriter_fourcc('M','J','P','G'), 30, self.size)

    def flick():
        pass
    
    def drawLine(self,image, x1, y1, x2, y2):
        thickness = 3
        lineColor = (0, 255, 0)
        dotColor = (255, 0, 0)
        radius = 8

        cv2.line(image, (x1,y1), (x2,y2), lineColor, thickness)
        cv2.circle(image, (x1,y1), radius, dotColor, -1)
        cv2.circle(image, (x2,y2), radius, dotColor, -1)

    def process(self,im):
        return cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    def export(self):
        print("Start exporting...")
        i = 0
        log = []
        while True:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, im = self.cap.read()
            f = 0
            for arr in self.myPoints:
                if (len(arr[i]) != 0):
                    for j in range(len(arr[i]) - 1):
                        self.drawLine(im, int(arr[i][j][0]), int(arr[i][j][1]), int(arr[i][j+1][0]), int(arr[i][j+1][1]))
                    cv2.imwrite(self.video + "Frame_"+str(i)+".jpg",im)
                    msg = (msgDesc[f], i)
                    log.append(msg)
                f += 1
            
            frameText = "Frame " + str(i)
            cv2.putText(im, frameText, (self.frameWidth-200, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
            self.result.write(im)
            if i == self.tots-1:
                break
            
            i+=1
            continue
        print("DONE!")
        self.result.release()
        return log