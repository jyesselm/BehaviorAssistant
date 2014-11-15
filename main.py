import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument('-p', help='program', required=True)
    parser.add_argument('-args', required=False)
    parser.add_argument('-files',required=False)
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    # Brief sketch follows
    args = parse_args()
    config = get_configuration()
    default_template = get_default_template(config)
    log = log.Log(config, default_template)

