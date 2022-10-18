import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Skeleton Extraction")
    parser.add_argument("-s", "--source", required=True, metavar='', help="path to the video or 0 to start camera capture")
    parser.add_argument("-d", "--device", type=str, default="cpu", metavar='', help="cpu or gpu")
    parser.add_argument("-m", "--model", type=str, default="COCO", metavar='', help="COCO, MPI, BODY_25")
    parser.add_argument("-t", "--thres", type=float, default=0.1, metavar='', help="Prediction threshold")
    args = parser.parse_args()
    return args