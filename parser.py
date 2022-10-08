import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Something")
    parser.add_argument("-s", "--source", required=True, metavar='', help="path to the video or 0 to start camera capture")
    parser.add_argument("-d", "--device", metavar='', help="cpu or gpu")
    parser.add_argument("-t", "--thres", metavar='', help="Prediction threshold")
    args = parser.parse_args()
    return args