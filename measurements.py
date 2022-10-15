from curses.ascii import RS
import math

# Distance formula returns distance between 2 points
def distance(p1, p2):
    d = math.sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))
    return d

# Law of Cosines returns angle at point 2
def law_cosines(p1, p2, p3):
    a = distance(p1, p2)
    b = distance(p2, p3) 
    c = distance(p1, p3)

    gamma = math.acos((pow(a, 2) + pow(b, 2) - pow(c, 2)) / (2 * a * b))
    
    degrees = gamma * 180 / math.pi

    return degrees


def get_frames(file):
    frames = []

    #Hard coded order of points to ensure compatibility with all versions of Python
    entries = ["nose", "neck", "Rshoulder", "Relbow", "Rwrist", "Lshoulder", "Lelbow", "Lwrist", "Rhip", "Rknee", "Rankle", "Lhip", "Lknee", "Lankle", "Reye", "Leye", "Rear", "Lear", "background"]

    f = open(file)

    for line in f:
        frame = {
            "nose" : (-1,-1),
            "neck" : (-1,-1),
            "Rshoulder" : (-1,-1),
            "Relbow" : (-1,-1),
            "Rwrist" : (-1,-1),
            "Lshoulder" : (-1,-1),
            "Lelbow" : (-1,-1),
            "Lwrist" : (-1,-1),
            "Rhip" : (-1,-1),
            "Rknee" : (-1,-1),
            "Rankle" : (-1,-1),
            "Lhip" : (-1,-1),
            "Lknee" : (-1,-1),
            "Lankle" : (-1,-1),
            "Reye" : (-1,-1),
            "Leye" : (-1,-1),
            "Rear" : (-1,-1),
            "Lear" : (-1,-1),
            "background" : (-1,-1)
        }
        point = 0
        line = line.replace('[','').replace(']','').replace('(','').replace(')','').split(",")
        line = [float(x) for x in line]
        for x in range(0,len(line) - 1,2):
            frame[entries[point]] = (line[x],line[x+1])
            point += 1
        frames.append(frame)
    
    return frames