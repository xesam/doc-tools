import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--version', '-v', action='version',
                    version='%(prog)s version : v 0.01',
                    help='show the version')

parser.add_argument('--debug', '-d',
                    action='store_true',
                    help='enable debug',
                    default=False)

args = parser.parse_args()
print("=== end ===")
