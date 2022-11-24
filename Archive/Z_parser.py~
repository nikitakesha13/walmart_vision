import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Skeleton Extraction")
    parser.add_argument("-n", "--name", type=str, metavar='', help="the name of the output file")
    parser.add_argument("-s", "--source", type=str, default="test-video/wyatt.mp4", metavar='', help="path to the video or 0 to start camera capture")
    parser.add_argument("-d", "--device", type=str, default="cpu", metavar='', help="cpu or gpu")
    parser.add_argument("-m", "--model", type=str, default="BODY_25", metavar='', help="COCO, MPI, BODY_25")
    parser.add_argument("-t", "--thres", type=float, default=0.1, metavar='', help="Prediction threshold")
    args = parser.parse_args()
    return args