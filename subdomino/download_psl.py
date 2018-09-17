"""
Download script for the Public Suffix List.
"""


import argparse
import shutil
import urllib.request


PSL_URL = 'https://publicsuffix.org/list/public_suffix_list.dat'
DEFAULT_PSL_OUT = 'psl.dat'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default=PSL_URL,
                        help='URL of Public Suffix List')
    parser.add_argument('--out-file', default=DEFAULT_PSL_OUT,
                        help='output file name')
    args = parser.parse_args()
    with urllib.request.urlopen(args.url) as response, open(args.out_file,
                                                            'wb') as out_file:
        shutil.copyfileobj(response, out_file)


if __name__ == '__main__':
    main()