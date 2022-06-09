"""

"""

import argparse

base_parser = argparse.ArgumentParser(add_help=False)
base_parser.add_argument('--version', '-v',
                         action='version',
                         version='%(prog)s version : v 0.01',
                         help='show the version')

doc_parser = argparse.ArgumentParser(description='doc')

sub_parsers = doc_parser.add_subparsers(help='commands')
split_parser = sub_parsers.add_parser('split', help='split document', parents=[])
split_parser.add_argument('--file', '-f',
                          help='set input filepath')
split_parser.add_argument('--page', '-p',
                          help='set pages')
split_parser.add_argument('--start', '-s',
                          help='set start pages')
split_parser.add_argument('--outfile', '-o',
                          help='set output file')
split_parser.add_argument('--outdir', '-d',
                          help='set output dir')

merge_parser = sub_parsers.add_parser('merge', help='merge documents', parents=[])

image_parser = sub_parsers.add_parser('image', help='translate document to image', parents=[])

args = doc_parser.parse_args()
print(args)
print("=== end ===")
