import argparse

def parse_boto3_args():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('--action', help='Which action you want to perform.', default=None)

    return parser
