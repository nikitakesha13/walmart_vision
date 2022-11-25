#Collection of helper functions that may be used many times
import math
import datetime

#---------------------------------------------------------------
#   GENERAL HELPERS
#---------------------------------------------------------------
def convertToLb(weight, unit):
    if (unit == "kg"):
        return weight * 2.20462262185
    return weight

def convertToInch(len, unit):
    if (unit == "cm"):
        return len * 0.3937007874
    if (unit == "ft"):
        return len * 12
    if (unit == "m"):
        return convertToInch(len * 100.0, "cm")
    return len
    
#strip leading and trailing zeroes
#convert spaces between into underscores
def cleanName(name):
    return ((name.strip()).replace(" ", "_")).lower()

def today(format):
    if format == 'hyphen':
        return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    elif format == 'slash':
        return datetime.datetime.now().strftime('%m/%d/%Y')


#---------------------------------------------------------------
#   NIOSH HELPERS
#   Compare and return the indices for individual measurements
#---------------------------------------------------------------
    
#run the horizontal distance to get the HM factor
def HMFactor(horizontialDist):
    hD = float(horizontialDist)
    if(hD >=  0) and (hD <= (25 * 2.54 )):
        return 1.0
    elif ( hD > (25 * 2.54 ) and hD <= (30 * 2.54 )):
        return 0.83
    elif (hD > (30 * 2.54 ) and hD <= (40 * 2.54 )):
        return 0.63
    elif(hD > (40 * 2.54 ) and hD <= (50 * 2.54 )):
        return 0.50
    elif(hD > (50 * 2.54 ) and hD <= (60 * 2.54 )):
        return 0.42
    else:
        return 0

#run the vertical distance to get the VM factor
def VMFactor(verticalDist):
    vD = float(verticalDist)
    if(vD >= 0 and vD < (30 * 2.54 )):
        return 1.0
    elif (vD >= (30* 2.54) and vD < (50 * 2.54 )):
        return 0.87
    elif (vD >= (50* 2.54) and vD < (70 * 2.54 )):
        return 0.93
    elif (vD >= (70* 2.54) and vD < (100 * 2.54 )):
        return 0.99
    elif (vD >= (100 * 2.54) and vD < (150 * 2.54 )):
        return 0.93
    elif (vD >= (150 * 2.54) and vD < (175 * 2.54 )):
        return 0.78
    elif (vD == (175* 2.54)):
        return 0.70
    else:
        return 0

#run the distance the load travels to get the DM factor
def DMFactor(distTravel):
    dT = float(distTravel)
    if(dT >= 0 and dT <= (25 * 2.54 )):
        return 1.0
    elif (dT > (25* 2.54) and dT <= (40 * 2.54 )):
        return 0.93
    elif (dT > (40* 2.54) and dT <= (55 * 2.54 )):
        return 0.90
    elif (dT > (55* 2.54) and dT <= (100 * 2.54 )):
        return 0.87
    elif (dT > (100* 2.54) and dT <= (175 * 2.54 )):
        return 0.85
    elif (dT > (175* 2.54)):
        return 0.0 

#run to equation to couplingMuti from user input into a number
def couplingMultiplier(CM):
    if CM == "Good":
        return 1.0
    elif CM == "Fair":
        return 2.0
    elif CM == "Poor":
        return 3.0


#---------------------------------------------------------------
#   ANALYSIS HELPERS
#   Process raw data and establish certain data structure to use in analysis
#---------------------------------------------------------------
    
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
            "nose" : None,
            "neck" : None,
            "Rshoulder" : None,
            "Relbow" : None,
            "Lshoulder" : None,
            "Lelbow" : None,
            "Rhip" : None,
            "Rknee" : None,
            "Lhip" : None,
            "Lknee" : None
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