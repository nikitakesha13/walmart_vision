import cv2
import time
import parser

# select if its front or side 
class Skeleton:
    def __init__(self, source, device = "cpu", model = "COCO", thres = 0.1):
        self.source = source
        self.device = device
        self.thres = thres

        if model == "BODY_25":
            print("Using BODY_25 model")
            self.BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
                        "LShoulder": 5, "LElbow": 6, "LWrist": 7, "MidHip": 8, "RHip": 9, "RKnee": 10,
                        "RAnkle": 11, "LHip": 12, "LKnee": 13, "LAnkle": 14, "REye": 15,
                        "LEye": 16, "REar": 17, "LEar": 18, "LBigToe": 19, "LSmallToe": 20, "LHeel": 21, 
                        "RBigToe": 22, "RSmallToe": 23, "RHeel": 24, "Background": 25 }

            self.POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
                        ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
                        ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
                        ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
                        ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"], ["LAnkle", "LBigToe"],
                        ["LAnkle", "LSmallToe"], ["LAnkle", "LHeel"], ["RAnkle", "RBigToe"], ["RAnkle", "RSmallToe"],
                        ["RAnkle", "RHeel"] ]

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

        else: # COCO is default model
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

        if (device == "gpu"):
            self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
            self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
        
        self.cap = cv2.VideoCapture(source)

        if (self.cap.isOpened() == False):
            print("Error opening file")

        self.frameWidth = int(self.cap.get(3))
        self.frameHeight = int(self.cap.get(4))

        size = (self.frameWidth, self.frameHeight)

        self.result = cv2.VideoWriter("test-video-out/out.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 30, size)
    
    def pose_estimation(self):

        frame_count = 0
        total_fps = 0
        
        while(True):

            print("Frame {} Processing".format(frame_count))

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

                # cv2.imshow('pose', frame)

                self.result.write(frame)

                print("Time to process frame in sec: " + str(end_time - start_time))
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    avg_fps = total_fps / frame_count
                    return avg_fps
            else :
                avg_fps = total_fps / frame_count
                return avg_fps
        
    def release(self):
        self.cap.release()
        self.result.release()
        cv2.destroyAllWindows() 


def main():
    args = parser.parse_args()
    if args.source == '0':
        args.source = 0

    skeleton = Skeleton(args.source, args.device, args.model)
    avg_fps = skeleton.pose_estimation()
    skeleton.release()

    print(f"Average FPS: {avg_fps:.3f}")
    

if __name__ == '__main__':
    main()