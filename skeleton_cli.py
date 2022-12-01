import argparse
from skeleton import Skeleton
from player import DrawVideo
from cli_player import CLI_Player
from form_analysis import *
from report_gen import Report

def parse_args():
    parser = argparse.ArgumentParser(description="Skeleton Extraction")
    parser.add_argument("-n", "--name", type=str, default="out", metavar='', help="the name of the output file")
    parser.add_argument("-s", "--source", type=str, default="test-video/wyatt.mp4", metavar='', help="path to the video or 0 to start camera capture")
    parser.add_argument("-d", "--device", type=str, default="cpu", metavar='', help="cpu or gpu")
    parser.add_argument("-m", "--model", type=str, default="BODY_25", metavar='', help="COCO, MPI, BODY_25")
    parser.add_argument("-t", "--thres", type=float, default=0.1, metavar='', help="Prediction threshold")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.source == '0':
        args.source = 0

    skeleton = Skeleton(args.name, args.source, args.device, args.model, args.thres)
    skeleton.pose_estimation()
    skeleton.release()
    print("REBA MAX score: " + str(skeleton.get_reba_max()))
    print("REBA average score: " + str(skeleton.get_reba_avg()))

    print("Average FPS: ", skeleton.get_average_fps())

    matrix = analysis(create_dicts(skeleton.get_form_analysis_matrix()))
    exp = DrawVideo(skeleton.get_path(), matrix)
    err = exp.export()

    report = Report(skeleton.get_path(), cleanName(args.name.capitalize()), today('slash'), skeleton.get_reba_avg(), skeleton.get_reba_max(), err[0])
    report.generate_report()

    play = CLI_Player(skeleton.get_path())
    play.cli_play()
    

if __name__ == '__main__':
    main()