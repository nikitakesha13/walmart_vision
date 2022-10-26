from measurements import *
# All analysis is being done from a side view
# (0,0) is top left corner

# OSHA Training: Keep your back straight while lifting
def check_spine(frames, tolerance):
    spine_status = []
    prev_spine = -1
    spine_length = -1
    for frame in frames:
        measurements = get_measurements(frame)
        spine_length = measurements["Spinal Length"]

        if (prev_spine == -1):
            prev_spine = spine_length
            continue

        if (spine_length - prev_spine < tolerance):
            spine_status.append("Good - Spinal Length")
        else:
            spine_status.append("Bad - Spinal Length")
        
        prev_spine = spine_length

    return spine_status

# OSHA Training: Do not overextend the spine backwards
def check_lean(frame, tolerance):
    facing = get_direction(frame)

    if get_measurements(frame)["Direction Facing"] == "R":
        if frame["Rshoulder"][0] - frame["Rhip"][0] > tolerance:
            return "Bad - Lean"
        else:
            return "Good - Lean"

    if get_measurements(frame)["Direction Facing"] == "L":
        if frame["Lshoulder"][0] - frame["Lhip"][0] > tolerance:
            return "Bad - Lean"
        else:
            return "Good - Lean"

# OSHA Training: Do not bend forward, instead squat down to an object
def check_knees(frames):
    knee_status = []
    for frame in frames:
        direction = get_measurements(frame)["Direction Facing"]
        knee,shoulder = -1
        prev_hip, prev_shoulder = -1
        
        if direction == "L":
            knee = frame["Lknee"]
            shoulder = frame["Lshoulder"]
        elif direction == "R":
            knee = frame["Rknee"]
            shoulder = frame["Rshoulder"]
        else:
            return knee_status
        
        if prev_shoulder == -1 or prev_knee == -1:
            prev_shoulder = shoulder
            prev_knee = knee
            continue
            

        # Check if shoulder is moving down
        if prev_shoulder[1] < shoulder[1]:
            if direction == "R" and knee[0] > prev_knee[0]:
                knee_status.append("Good - Knees")
            elif direction == "L" and knee[0] < prev_knee[0]:
                knee_status.append("Good - Knees")
            else:
                knee_status.append("Bad - Knees")
    return knee_status

# OSHA Taining Check: Should not lift an object above shoulder level
def check_elbows(frame):
    if frame["Relbow"][1] > frame["Rshoulder"][1]:
        return "Bad - Arms"
    if frame["Lelbow"][1] > frame["Lshoulder"][1]:
        return "Bad - Arms"

    return "Good - Arms"



def analysis(frames):
    tolerance = 5
    # Individual frame checks
    elbow_height_frames = []
    back_lean_frames = []
    for frame in frames:
        elbow_height_frames.append(check_elbows(frame))
        back_lean_frames.append(check_lean(frame, tolerance))
    # Multiple frame checks
    spine_length_frames = check_spine(frames, tolerance)
    knees_bent_frames = check_knees(frames)

    # Creare analysis output
    output = open("analysis_results.txt", "w")
    for x in range(len(elbow_height_frames)):
        output.write(spine_length_frames[x])
        output.write(back_lean_frames[x])
        output.write(knees_bent_frames[x])
        output.write(elbow_height_frames[x])
        output.write("")
