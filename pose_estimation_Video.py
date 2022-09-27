import cv2

# select if its front or side 

protoFile = "pose/coco/pose_deploy_linevec.prototxt"
weightsFile = "pose/coco/pose_iter_440000.caffemodel"


BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

# net = cv2.dnn.readNetFromTensorflow("graph_opt.pb")
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

# Use when graph_out.pb
# thres = 0.45

# Use when coco
thres = 0.1

# cap = cv2.VideoCapture("test-video/DeadliftCrop.mp4")

# To capture video right now, comment above and use below
cap = cv2.VideoCapture(0)

if (cap.isOpened() == False):
    print("Error opening file")

frameWidth = int(cap.get(3))
frameHeight = int(cap.get(4))

size = (frameWidth, frameHeight)

result = cv2.VideoWriter("test-video-out/out.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 10, size)

def pose_estimation():
    
    while(True):
        
        ret, frame = cap.read()

        if ret == True:
        
            # net.setInput(cv2.dnn.blobFromImage(frame, 1.0, (368, 368), (127.5, 127.5, 127.5), swapRB=True, crop=False))
            net.setInput(cv2.dnn.blobFromImage(frame, 1.0 / 255, (368, 368), (0, 0, 0), swapRB=False, crop=False))
        
            out = net.forward()
            out = out[:, :19, :, :]
        
            assert(len(BODY_PARTS) == out.shape[1])
        
            points = []
            
            
            for i in range(len(BODY_PARTS)):
                # Slice heatmap of corresponging body's part.
                heatMap = out[0, i, :, :]

                _, conf, _, point = cv2.minMaxLoc(heatMap)
                x = (frameWidth * point[0]) / out.shape[3]
                y = (frameHeight * point[1]) / out.shape[2]
                points.append((int(x), int(y)) if conf > thres else None)
                
            for pair in POSE_PAIRS:
                partFrom = pair[0]
                partTo = pair[1]
                assert(partFrom in BODY_PARTS)
                assert(partTo in BODY_PARTS)

                idFrom = BODY_PARTS[partFrom]
                idTo = BODY_PARTS[partTo]
                
                if points[idFrom] and points[idTo]:
                    cv2.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
                    cv2.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                    cv2.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
                    cv2.putText(frame, str(partTo), points[idTo], cv2.FONT_HERSHEY_PLAIN, 1.0, (0,0,255), 2)
            
            result.write(frame)

            cv2.imshow('pose', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else :
            break
    
        
    
pose_estimation()

cap.release()
result.release()

cv2.destroyAllWindows()            