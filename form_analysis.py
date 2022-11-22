from measurements import *
# All analysis is being done from a side view
# (0,0) is top left corner

# OSHA Training: Keep your back straight while lifting
def check_spine(frames, tolerance):
    spine_status = []
    prev_spine = -1
    spine_length = -1
    for frame in frames:
        spine_length = get_spine_length(frame)

        # Results are inconclusive
        if (prev_spine == -1):
            prev_spine = spine_length
            spine_status.append("Inconclusive - Spine Length")
            continue
        
        # Results are positive
        if (spine_length - prev_spine < tolerance):
            spine_status.append("Good - Spine Length")

        # Results are negative
        else:
            tailbone = ((frame["Lhip"][0] + frame["Rhip"][0]) / 2, (frame["Lhip"][1] + frame["Rhip"][1]) / 2)
            spine_status.append("Bad - " + str(tailbone[0]) + " " + str(tailbone[1]) + " " + str(frame["neck"][0]) + " " + str(frame["neck"][1]) + " 1 ")
        
        prev_spine = spine_length

    return spine_status

# OSHA Training: Do not overextend the spine backwards
def check_lean(frame, tolerance):
    facing = get_direction(frame)

    if get_direction(frame) == "R":
        if frame["Rshoulder"][0] - frame["Rhip"][0] > tolerance:
            return "Bad - " + str(frame["Rshoulder"][0]) + " " + str(frame["Rshoulder"][1]) + " " + str(frame["Rhip"][0]) + " " + str(frame["Rhip"][1]) + " 2 "
        else:
            return "Good - Lean"

    if get_direction(frame) == "L":
        if frame["Lshoulder"][0] - frame["Lhip"][0] > tolerance:
            return "Bad - " + str(frame["Lshoulder"][0]) + " " + str(frame["Lshoulder"][1]) + " " + str(frame["Lhip"][0]) + " " + str(frame["Lhip"][1]) + " 2 "
        else:
            return "Good - Lean"

# OSHA Training: Do not bend forward, instead squat down to an object
def check_knees(frames, tolerance):
    knee_status = []
    knee = -1
    shoulder = -1
    prev_shoulder = -1
    for frame in frames:
        direction = get_direction(frame)
        
        if direction == "L":
            knee = frame["Lknee"]
            shoulder = frame["Lshoulder"]
        elif direction == "R":
            knee = frame["Rknee"]
            shoulder = frame["Rshoulder"]
        else:
            knee_status.append("Inconclusive - Knees")
            continue
        
        if prev_shoulder == -1 or prev_knee == -1:
            prev_shoulder = shoulder
            prev_knee = knee
            knee_status.append("Inconclusive - Knees")
            continue
            

        # Check if shoulder is moving down
        if prev_shoulder[1] < shoulder[1]:
            if direction == "R" and knee[0] - prev_knee[0] < tolerance:
                knee_status.append("Good - Knees")
            else:
                if direction == "R":
                    hip = frame["Rhip"]
                else:
                    hip = frame["Lhip"]

                knee_status.append("Bad - " + str(knee[0]) + " " + str(knee[1]) + " " + str(hip[0]) + " " + str(hip[1]) + " 3 ")
        else:
            knee_status.append("Good - Knees")

    return knee_status

# OSHA Taining Check: Should not lift an object above shoulder level
def check_elbows(frame):
    if frame["Relbow"][1] < frame["Rshoulder"][1]:
        return "Bad - " + str(frame["Relbow"][0]) + " " + str(frame["Relbow"][1]) + " " + str(frame["Rshoulder"][0]) + " " + str(frame["Rshoulder"][1]) + " 4 "
    if frame["Lelbow"][1] < frame["Lshoulder"][1]:
        return "Bad - " + str(frame["Lelbow"][0]) + " " + str(frame["Lelbow"][1]) + " " + str(frame["Lshoulder"][0]) + " " + str(frame["Lshoulder"][1]) + " 4 "

    return "Good - Arms"


def analysis(frames):
    tolerance = 20
    # Individual frame checks
    elbow_height_frames = []
    back_lean_frames = []
    for frame in frames:
        elbow_height_frames.append(check_elbows(frame))
        back_lean_frames.append(check_lean(frame, tolerance))
    # Multiple frame checks
    spine_length_frames = check_spine(frames, tolerance)
    knees_bent_frames = check_knees(frames, tolerance)

    # Creare analysis output
    output = open("analysis_results.txt", "w")
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
        output.write(str(num_bad) + " ")
        output.write(frame)


# Testing
analysis(get_frames("points.txt"))
