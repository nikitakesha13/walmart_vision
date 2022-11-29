import cv2
import time
import datetime
import REBA
from misc import *
import os

# select if its front or side 
class Skeleton:
    def __init__(self, name, source, device, model, thres):

        print("Using " + device)
        self.path = "test-video-out/" + name + "_" + today('hyphen') + "/"

        try:
            os.mkdir(self.path)
        except OSError as error:
            print(error)
            
        self.skeleton_name = self.path + "skeleton.avi"
        self.form_analysis_name = self.path + "form_analysis.avi"

        self.source = source
        self.device = device
        self.thres = thres
        self.model = model
        self.average_fps = 0
        self.reba_max = 0
        self.reba_avg = 0
        self.form_analysis_matrix = []
        self.reba_arr = []

        if model == "BODY_25" or model == "COCO" :
            element_zero = "Nose"
            if model == "BODY_25" :
                print("Using BODY_25 model")
                protoFile = "pose/body_25/pose_deploy.prototxt"
                weightsFile = "pose/body_25/pose_iter_584000.caffemodel"
            else :
                print("Using COCO model")
                protoFile = "pose/coco/pose_deploy_linevec.prototxt"
                weightsFile = "pose/coco/pose_iter_440000.caffemodel"

        elif model == "MPI" :
            element_zero = "Head"
            print("Using MPI model")
            protoFile = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
            weightsFile = "pose/mpi/pose_iter_160000.caffemodel"
        
        else :
            print("The model does not exist. Possible models: COCO, MPI, BODY_25")
            exit(0)

        self.BODY_PARTS = { element_zero: 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                        "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                        "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13 }

        self.POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                        ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                        ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                        ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", element_zero] ]

        self.net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

        if (device == "gpu"):
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        
        self.cap = cv2.VideoCapture(source)

        if (self.cap.isOpened() == False):
            print("Error opening file")

        self.frameWidth = int(self.cap.get(3))
        self.frameHeight = int(self.cap.get(4))

        print("Width: " + str(self.frameWidth))
        print("Length: " + str(self.frameHeight))

        size = (self.frameWidth, self.frameHeight)

        self.result = cv2.VideoWriter(self.skeleton_name, cv2.VideoWriter_fourcc('M','J','P','G'), 30, size)
        self.form_analysis = cv2.VideoWriter(self.form_analysis_name, cv2.VideoWriter_fourcc('M','J','P','G'), 30, size)
    
    def pose_estimation(self):

        frame_count = 0
        total_fps = 0
        print("Skeleton extraction begins...")

        cv2.namedWindow("Display", cv2.WINDOW_AUTOSIZE)
        
        while(True):

            start_time = time.time()
            ret, frame = self.cap.read()

            if ret == True:
                self.net.setInput(cv2.dnn.blobFromImage(frame, 1.0 / 255, (368, 368), (0, 0, 0), swapRB=False, crop=False))
                out = self.net.forward()
                points = []

                size = 26
                if self.model == "MPI" :
                    size = 16
                elif self.model == "COCO" :
                    size = 19

                for i in range(size):
                    # Slice heatmap of corresponging body's part.
                    if self.model == "BODY_25" and (i == 8 or (i >= 15 and i <= 25)) :
                        continue

                    if self.model == "COCO" and (i >= 14 and i <= 18):
                        continue

                    if self.model == "MPI" and (i == 14 or i == 15) :
                        continue

                    heatMap = out[0, i, :, :]

                    _, conf, _, point = cv2.minMaxLoc(heatMap)
                    x = (self.frameWidth * point[0]) / out.shape[3]
                    y = (self.frameHeight * point[1]) / out.shape[2]
                    points.append((int(x), int(y)) if conf > self.thres else None)

                self.form_analysis_matrix.append(points[:4] + points[5:7] + points[8:10] + points[11:13])

                reba = REBA.REBA(points, self.model)
                reba_calculation = (reba.calculate_risk())
                if reba_calculation != None :
                    cv2.putText(frame, "REBA Score: " + str(reba_calculation[0]), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255,0,0), 2)
                    # reba_calculation = list(reba_calculation)
                    # reba_calculation[1] = (reba_calculation[1].split(".", 1))[0]
                    # reba_calculation = tuple(reba_calculation)
                    self.reba_arr.append(int(reba_calculation[0]))
                
                self.form_analysis.write(frame)

                for pair in self.POSE_PAIRS:
                    partFrom = pair[0]
                    partTo = pair[1]
                    assert(partFrom in self.BODY_PARTS)
                    assert(partTo in self.BODY_PARTS)

                    idFrom = self.BODY_PARTS[partFrom]
                    idTo = self.BODY_PARTS[partTo]
                    
                    if points[idFrom] and points[idTo]:
                        cv2.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
                        cv2.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                        cv2.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                        cv2.putText(frame, str(partFrom), points[idFrom], cv2.FONT_HERSHEY_PLAIN, 1.0, (0,0,255), 2)

                end_time = time.time()
                fps = 1 / (end_time - start_time)
                total_fps += fps
                frame_count += 1

                self.result.write(frame)
                cv2.imshow("Display", frame)
                key = cv2.waitKey(1)
                
                if key == ord('q') or key == 27 or (cv2.getWindowProperty('Display', cv2.WND_PROP_AUTOSIZE) < 0):
                    break
            else :
                break

        self.average_fps = total_fps / frame_count
        if len(self.reba_arr) > 0 :
            self.reba_max = max(self.reba_arr)
            sum_reba = sum(self.reba_arr)
            self.reba_avg = round(sum_reba / len(self.reba_arr))
        
        return [self.get_average_fps(), self.get_reba_max(), self.get_reba_avg(), self.get_path()]

    def get_reba_msg(self, reba_score):
        if reba_score == 0 or reba_score == 1:
            return "Negligible Risk"
        elif reba_score == 2 or reba_score == 3:
            return "Low Risk"
        elif reba_score >= 4 and reba_score <= 7:
            return "Medium Risk"
        elif reba_score >= 8 and reba_score <= 10:
            return "High Risk"
        return "Very High Risk"

    def get_reba_max(self):
        return (self.reba_max, self.get_reba_msg(self.reba_max))
    
    def get_reba_avg(self):
        return (self.reba_avg, self.get_reba_msg(self.reba_avg))
    
    def get_form_analysis_matrix(self):
        return self.form_analysis_matrix
    
    def get_average_fps(self):
        return self.average_fps
    
    def get_path(self):
        return self.path
        
    def release(self):
        self.cap.release()
        self.result.release()
        self.form_analysis.release()
        cv2.destroyAllWindows() 