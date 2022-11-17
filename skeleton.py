import cv2
import time
import datetime
import REBA
import os

# select if its front or side 
class Skeleton:
    def __init__(self, name, source, device, model, thres):

        time_now = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        path = "test-video-out/" + name + "_" + time_now + "/"

        try:
            os.mkdir(path)
        except OSError as error:
            print(error)
            
        self.skeleton_name = path + "skeleton.avi"
        self.original_name = path + "original.avi"
        self.form_analysis_name = path + "form_analysis.avi"

        self.source = source
        self.device = device
        self.thres = thres
        self.model = model
        self.reba_arr = []
        self.file = open(path + "points.txt", "w")

        if model == "BODY_25" or model == "COCO":

            self.BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                        "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
                        "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
                        "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

            self.POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                        ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                        ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                        ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                        ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

            if model == "BODY_25":
                print("Using BODY_25 model")
                protoFile_body_25 = "pose/body_25/pose_deploy.prototxt"
                weightsFile_body_25 = "pose/body_25/pose_iter_584000.caffemodel"
                self.net = cv2.dnn.readNetFromCaffe(protoFile_body_25, weightsFile_body_25)
            else :
                print("Using COCO model")
                protoFile_coco = "pose/coco/pose_deploy_linevec.prototxt"
                weightsFile_coco = "pose/coco/pose_iter_440000.caffemodel"
                self.net = cv2.dnn.readNetFromCaffe(protoFile_coco, weightsFile_coco)

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

        self.result = cv2.VideoWriter(self.skeleton_name, cv2.VideoWriter_fourcc('M','J','P','G'), 30, size)
        self.original = cv2.VideoWriter(self.original_name, cv2.VideoWriter_fourcc('M','J','P','G'), 30, size)
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
                self.original.write(frame)

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
                    if self.model == "BODY_25" and (i == 8 or (i > 18 and i < 25)) :
                        continue

                    heatMap = out[0, i, :, :]

                    _, conf, _, point = cv2.minMaxLoc(heatMap)
                    x = (self.frameWidth * point[0]) / out.shape[3]
                    y = (self.frameHeight * point[1]) / out.shape[2]
                    points.append((int(x), int(y)) if conf > self.thres else None)

                # Write the points to file for analysis
                self.file.write(str(points) + '\n')

                reba_points = points.copy()
                reba = REBA.REBA(reba_points, self.model)
                reba_calculation = reba.calculate_risk()
                if reba_calculation != None :
                    cv2.putText(frame, "REBA Score: " + str(reba_calculation[0]), (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.75, (255,0,0), 2)
                    self.reba_arr.append(reba_calculation)
                
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
                    avg_fps = total_fps / frame_count
                    if len(self.reba_arr) > 0 :
                        max_index = self.reba_arr.index(max(self.reba_arr, key=lambda x:x[0]))
                        min_index = self.reba_arr.index(min(self.reba_arr, key=lambda x:x[0]))
                        print("Max REBA score: ", self.reba_arr[max_index][0],  self.reba_arr[max_index][1])
                        print("Min REBA score: ", self.reba_arr[min_index][0], self.reba_arr[min_index][1])
                    return [avg_fps, reba_max, reba_avg]
            else :
                avg_fps = total_fps / frame_count
                if len(self.reba_arr) > 0 :
                    max_index = self.reba_arr.index(max(self.reba_arr, key=lambda x:x[0]))
                    min_index = self.reba_arr.index(min(self.reba_arr, key=lambda x:x[0]))
                    print("Max REBA score: ", self.reba_arr[max_index][0],  self.reba_arr[max_index][1])
                    print("Min REBA score: ", self.reba_arr[min_index][0], self.reba_arr[min_index][1])
                return avg_fps
        
    def release(self):
        self.cap.release()
        self.result.release()
        self.original.release()
        self.form_analysis.release()
        cv2.destroyAllWindows() 
        self.file.close()