import math

# Distance formula returns distance between 2 points
def distance(p1, p2):
    d = math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
    return d

# Dictionaries are created to allow for ease of future edits
# If in future points were entered differently then all that would need to be created for
# compatibility is dictionaries for each frame
def create_dicts(matrix):
    frames = []

    # Hard coded order of points to ensure dictionary compatibility with all versions of Python
    entries = ["nose", "neck", "Rshoulder", "Relbow", "Lshoulder", "Lelbow", "Rhip", "Rknee", "Lhip", "Lknee"]

    for entry in matrix:
        frame = {
            "nose" : (-1,-1),
            "neck" : (-1,-1),
            "Rshoulder" : (-1,-1),
            "Relbow" : (-1,-1),
            "Lshoulder" : (-1,-1),
            "Lelbow" : (-1,-1),
            "Rhip" : (-1,-1),
            "Rknee" : (-1,-1),
            "Lhip" : (-1,-1),
            "Lknee" : (-1,-1),
        }
        point = 0
        for x in entry:
            frame[entries[point]] = x
            point += 1
        frames.append(frame)
    
    return frames

def get_direction(frame):
    nose = frame["nose"]
    neck = frame["neck"]

    if (nose[0] >neck[0]):
        return "R"
    elif (nose[0] < neck[0]):
        return "L"
    else:
        return "F"

def get_spine_length(frame):
    tailbone = ((frame["Lhip"][0] + frame["Rhip"][0]) / 2, (frame["Lhip"][1] + frame["Rhip"][1]) / 2)
    return distance(tailbone, frame["neck"])

# Testing
# mat = [[(1,1),(2,2),(3,3),None,(5,5),(6,6),(7,7),(8,8),(9,9),(10,10)]]
# print(create_dicts(mat))