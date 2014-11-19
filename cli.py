import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="")

    #one of these needs to be activated present, each run requires a message for logging!
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("--message","-m",help="log message")
    group.add_argument("--message_file", "-mf", help="log message file")

    parser.add_argument("--command","-c", help="command", required=False)
    parser.add_argument("--since", type=str, default=None)
    parser.add_argument("--until", type=str, default=None)
    parser.add_argument("--render", type=str, default=None)
    parser.add_argument("--renderout", "-ro", type=argparse.FileType("w"), default=open("ba_render.out", "w"), required=False)
    parser.add_argument("-args", required=False)
    parser.add_argument("-files",required=False)
    args = parser.parse_args()
    return args


def parse_cli():
    args = parse_args()
    return args

