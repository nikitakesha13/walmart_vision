from measurements import *
# All analysis is being done from a side view
# (0,0) is top left corner

# OSHA Training: Keep your back straight while lifting
def check_spine(frames, tolerance):
    spine_status = []
    prev_spine = -1
    spine_length = -1
    for frame in frames:
        # Error Checking
        if frame["Rhip"] == None or \
           frame["Lhip"] == None or \
           frame["neck"] == None:
            spine_status.append([])
            continue

        spine_length = get_spine_length(frame)

        # Results are inconclusive
        if (prev_spine == -1):
            prev_spine = spine_length
            spine_status.append([])
            continue
        
        # Results are positive
        if (spine_length - prev_spine < tolerance):
            spine_status.append([])

        # Results are negative
        else:
            tailbone = (int((frame["Lhip"][0] + frame["Rhip"][0]) / 2), int((frame["Lhip"][1] + frame["Rhip"][1]) / 2))
            spine_status.append([tailbone, frame["neck"]])
        
        prev_spine = spine_length

    return spine_status

# OSHA Training: Do not overextend the spine backwards
def check_lean(frame, tolerance):
    # Error Checking
    if frame["Rshoulder"] == None or \
       frame["Rhip"] == None or \
       frame["Lshoulder"] == None or \
       frame["Lhip"] == None or \
       frame["neck"] == None or \
       frame["nose"] == None:
        return []

    facing = get_direction(frame)

    if facing == "R":
        if frame["Rshoulder"][0] - frame["Rhip"][0] > tolerance:
            return [frame["Rshoulder"], frame["Rhip"]]
        else:
            return []

    if facing == "L":
        if frame["Lshoulder"][0] - frame["Lhip"][0] > tolerance:
            return [frame["Lshoulder"], frame["Lhip"]]
        else:
            return []

# OSHA Training: Do not bend forward, instead squat down to an object
def check_knees(frames, tolerance):
    knee_status = []
    knee = -1
    shoulder = -1
    prev_shoulder = -1
    for frame in frames:
        # Error Checking
        if frame["Lknee"] == None or \
           frame["Lshoulder"] == None or \
           frame["Lhip"] == None or \
           frame["Rknee"] == None or \
           frame["Rshoulder"] == None or \
           frame["Rhip"] == None or \
           frame["nose"] == None or \
           frame["neck"] == None:
            knee_status.append([])
            continue

        direction = get_direction(frame)
        
        if direction == "L":
            knee = frame["Lknee"]
            shoulder = frame["Lshoulder"]
        elif direction == "R":
            knee = frame["Rknee"]
            shoulder = frame["Rshoulder"]
        else:
            knee_status.append([])
            continue
        
        if prev_shoulder == -1 or prev_knee == -1:
            prev_shoulder = shoulder
            prev_knee = knee
            knee_status.append([])
            continue
            

        # Check if shoulder is moving down
        if prev_shoulder[1] < shoulder[1]:
            if direction == "R" and knee[0] - prev_knee[0] < tolerance:
                knee_status.append([])
            elif direction == "L" and prev_knee[0] - knee[0] < tolerance:
                knee_status.append([])
            else:
                if direction == "R":
                    hip = frame["Rhip"]
                else:
                    hip = frame["Lhip"]

                knee_status.append([knee, hip])
        else:
            knee_status.append([])

    return knee_status

# OSHA Taining Check: Should not lift an object above shoulder level
def check_elbows(frame):
    # Error Checking
    if frame["Relbow"] == None or \
       frame["Rshoulder"] == None or \
       frame["Lelbow"] == None or \
       frame["Lshoulder"] == None:
        return []
    #
    if frame["Relbow"][1] < frame["Rshoulder"][1]:
        return [frame["Relbow"], frame["Rshoulder"]]
    if frame["Lelbow"][1] < frame["Lshoulder"][1]:
        return [frame["Lelbow"], frame["Lshoulder"]]

    return []


def analysis(frames):
    # Individual frame checks
    elbow_height_frames = []
    back_lean_frames = []
    for frame in frames:
        elbow_height_frames.append(check_elbows(frame))
        back_lean_frames.append(check_lean(frame, 20))
    # Multiple frame checks
    spine_length_frames = check_spine(frames, 20)
    knees_bent_frames = check_knees(frames, 0)

    # Creare analysis output
    for x in range(len(elbow_height_frames)):
        frame = ""
        num_bad = 0
        if spine_length_frames[x][0:3] == "Bad":
            frame += spine_length_frames[x][6:]
            num_bad += 1
        if back_lean_frames[x][0:3] == "Bad":
            frame += back_lean_frames[x][6:]
            num_bad += 1
        if knees_bent_frames[x][0:3] == "Bad":
            frame += knees_bent_frames[x][6:]
            num_bad += 1
        if elbow_height_frames[x][0:3] == "Bad":
            frame+= elbow_height_frames[x][6:]
            num_bad += 1
        frame += "\n"

    return [elbow_height_frames, back_lean_frames, spine_length_frames, knees_bent_frames]


# Testing
input = [[(584, 31), None, None, None, (667, 78), (667, 172), (612, 281), (612, 281), None, (640, 281)],
[(584, 31), (640, 78), None, None, (640, 78), (667, 172), (612, 266), (612, 266), None, (640, 281)],
[(556, 31), None, None, None, (640, 78), (667, 172), (612, 281), (612, 281), None, (640, 281)],
[(556, 46), None, None, None, (640, 78), (667, 172), (612, 281), (612, 281), None, (640, 281)],
[(556, 46), (640, 93), None, None, (640, 93), (667, 172), (612, 281), (612, 281), None, (640, 281)],
[(556, 46), (640, 93), None, None, (640, 93), (667, 187), (612, 281), (612, 281), None, (640, 281)],
[(556, 46), (640, 93), None, None, (640, 93), (667, 172), (612, 281), (612, 281), None, (640, 281)],
[(556, 46), None, None, None, (640, 78), (667, 172), (612, 281), None, None, (640, 281)]]

matrix = analysis(create_dicts(input))

for row in matrix:
    print (row)
    print ("\n")
