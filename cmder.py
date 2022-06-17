"""

"""

import argparse

base_parser = argparse.ArgumentParser(add_help=False)
base_parser.add_argument('--version', '-v',
                         action='version',
                         version='%(prog)s version : v 0.01',
                         help='show the version')

main_parser = argparse.ArgumentParser(description='doc tools')
sub_parsers = main_parser.add_subparsers(help='commands')

split_parser = sub_parsers.add_parser('split', help='split document', parents=[])
split_parser.add_argument('--file', '-f',
                          required=True,
                          nargs='+',
                          dest='files',
                          help='set input files')

# split_parser.add_argument('files',
#                           help='set input files')


split_mode_group = split_parser.add_mutually_exclusive_group(required=True)
split_mode_group.add_argument('--page', '-p',
                              nargs='+',
                              help='set pages range')
split_mode_group.add_argument('--start', '-s',
                              nargs='+',
                              help='set start pages')

quick_page_group = split_parser.add_mutually_exclusive_group()
quick_page_group.add_argument('-odd',
                              action='store_true',
                              dest='odd',
                              help='select all odd pages')
quick_page_group.add_argument('-even',
                              action='store_true',
                              dest='even',
                              help='select all even pages')

out_group = split_parser.add_mutually_exclusive_group(required=True)
out_group.add_argument('--outfile', '-o',
                       help='set output file')
out_group.add_argument('--outdir', '-d',
                       help='set output dir')

merge_parser = sub_parsers.add_parser('merge', help='merge documents', parents=[])

image_parser = sub_parsers.add_parser('image', help='translate document to image', parents=[])

args = main_parser.parse_args()
print(args)
