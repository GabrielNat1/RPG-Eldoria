import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true', help='Activate development mode')
args = parser.parse_args()
dev_mode = args.dev
