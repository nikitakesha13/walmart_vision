import cv2
import time
import datetime

from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

# select if its front or side 
class Skeleton:
    def __init__(self, name, source, device, model, thres, gui):

        self.name = "test-video-out/"
        if name == None:
            self.name += datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        else :
            self.name += name
            
        self.name += "_skeleton.avi"

        self.source = source
        self.device = device
        self.thres = thres
        self.file = open("points.txt", "w")
        self.gui = gui

        if model == "BODY_25":
            print("Using BODY_25 model")

            self.BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                        "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 9, "RKnee": 10,
                        "RAnkle": 11, "LHip": 12, "LKnee": 13, "LAnkle": 14, "REye": 15,
                        "LEye": 16, "REar": 17, "LEar": 18, "Background": 25 }

            self.POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                        ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                        ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                        ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                        ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

            # ==================================================================================================
            # The original BODY_25 points
            # self.BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
            #             "LShoulder": 5, "LElbow": 6, "LWrist": 7, "MidHip": 8, "RHip": 9, "RKnee": 10,
            #             "RAnkle": 11, "LHip": 12, "LKnee": 13, "LAnkle": 14, "REye": 15,
            #             "LEye": 16, "REar": 17, "LEar": 18, "LBigToe": 19, "LSmallToe": 20, "LHeel": 21, 
            #             "RBigToe": 22, "RSmallToe": 23, "RHeel": 24, "Background": 25 }

            # self.POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
            #             ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
            #             ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
            #             ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
            #             ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"], ["LAnkle", "LBigToe"],
            #             ["LAnkle", "LSmallToe"], ["LAnkle", "LHeel"], ["RAnkle", "RBigToe"], ["RAnkle", "RSmallToe"],
            #             ["RAnkle", "RHeel"] ]
            # ==================================================================================================

            protoFile_body_25 = "pose/body_25/pose_deploy.prototxt"
            weightsFile_body_25 = "pose/body_25/pose_iter_584000.caffemodel"
            self.net = cv2.dnn.readNetFromCaffe(protoFile_body_25, weightsFile_body_25)

        elif model == "MPI": # requires higher threshold
            print("Using MPI model")
            self.BODY_PARTS = { "Head": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                        "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                        "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "Chest": 14, "Background": 15 }

            self.POSE_PAIRS = [ ["Head", "Neck"], ["Neck", "RShoulder"], ["RShoulder", "RElbow"],
                                ["RElbow", "RWrist"], ["Neck", "LShoulder"], ["LShoulder", "LElbow"],
                                ["LElbow", "LWrist"], ["Neck", "Chest"], ["Chest", "RHip"], ["RHip", "RKnee"],
                                ["RKnee", "RAnkle"], ["Chest", "LHip"], ["LHip", "LKnee"], ["LKnee", "LAnkle"] ]

            protoFile_mpi = "pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
            weightsFile_mpi = "pose/mpi/pose_iter_160000.caffemodel"
            self.net = cv2.dnn.readNetFromCaffe(protoFile_mpi, weightsFile_mpi)

        elif model == "COCO": # COCO is default model
            print("Using COCO model")
            self.BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                        "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                        "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                        "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

            self.POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                        ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                        ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                        ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                        ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

            protoFile_coco = "pose/coco/pose_deploy_linevec.prototxt"
            weightsFile_coco = "pose/coco/pose_iter_440000.caffemodel"
            self.net = cv2.dnn.readNetFromCaffe(protoFile_coco, weightsFile_coco)
        
        else:
            print("The model does not exist. Possible models: COCO, MPI, BODY_25")
            exit(0)

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

        self.result = cv2.VideoWriter(self.name, cv2.VideoWriter_fourcc('M','J','P','G'), 30, size)
    
    def pose_estimation(self):

        frame_count = 0
        total_fps = 0
        
        while(True):
            start_time = time.time()
            
            ret, frame = self.cap.read()

            if ret == True:

                self.net.setInput(cv2.dnn.blobFromImage(frame, 1.0 / 255, (368, 368), (0, 0, 0), swapRB=False, crop=False))
                out = self.net.forward()
                points = []

                for i in range(len(self.BODY_PARTS)):
                    # Slice heatmap of corresponging body's part.
                    heatMap = out[0, i, :, :]

                    _, conf, _, point = cv2.minMaxLoc(heatMap)
                    x = (self.frameWidth * point[0]) / out.shape[3]
                    y = (self.frameHeight * point[1]) / out.shape[2]
                    points.append((int(x), int(y)) if conf > self.thres else None)

                # Write the points to file for analysis
                self.file.write(str(points) + '\n')

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
                        cv2.putText(frame, str(partTo), points[idTo], cv2.FONT_HERSHEY_PLAIN, 1.0, (0,0,255), 2)

                end_time = time.time()
                fps = 1 / (end_time - start_time)
                total_fps += fps
                frame_count += 1
                
                img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888).rgbSwapped()
                img = img.scaled(1280, 720, Qt.KeepAspectRatio)
                pix = QPixmap.fromImage(img)
                self.gui.videoView.setPixmap(pix)

                self.result.write(frame)
                if (cv2.waitKey(1) == ord('q')):
                    return -1

    def release(self):
        self.cap.release()
        self.result.release()
        self.file.close()