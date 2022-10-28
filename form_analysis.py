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

        if (prev_spine == -1):
            prev_spine = spine_length
            spine_status.append("Inconclusive - Spinal Length")
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

    if get_direction(frame) == "R":
        if frame["Rshoulder"][0] - frame["Rhip"][0] > tolerance:
            return "Bad - Lean: R Shoulder X =" + str(frame["Rshoulder"][0]) + "  Hip X = " + str(frame["Rhip"][0])
        else:
            return "Good - Lean"

    if get_direction(frame) == "L":
        if frame["Lshoulder"][0] - frame["Lhip"][0] > tolerance:
            return "Bad - Lean: L Shoulder X =" + str(frame["Lshoulder"][0]) + "  Hip X = " + str(frame["Lhip"][0])
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
            elif direction == "L" and knee[0] - prev_knee[0] < tolerance:
                knee_status.append("Good - Knees")
            else:
                knee_status.append("Bad - Knees")
        else:
            knee_status.append("Good - Knees")

    return knee_status

# OSHA Taining Check: Should not lift an object above shoulder level
def check_elbows(frame):
    if frame["Relbow"][1] < frame["Rshoulder"][1]:
        return "Bad - Arms"
    if frame["Lelbow"][1] < frame["Lshoulder"][1]:
        return "Bad - Arms"

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
        output.write(spine_length_frames[x]+"\n")
        output.write(back_lean_frames[x]+"\n")
        output.write(knees_bent_frames[x]+"\n")
        output.write(elbow_height_frames[x]+"\n")
        output.write("\n")

# Testing
analysis(get_frames("points.txt"))
