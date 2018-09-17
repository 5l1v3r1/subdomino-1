"""
Main driver for subdomino, the subdomain analysis utility.
"""

# Standard library imports
import argparse
import sys

# Other imports from this project
import dist_filter
import site_filter
import subdomain_list_filter
import suffix_filter


FILTERS = {
    'filter': suffix_filter.SuffixFilter,
    'site': site_filter.SiteFilter,
    'subdomain': subdomain_list_filter.SubdomainListFilter,
    'dist': dist_filter.DistFilter,
}


def parse(args=sys.argv):
    parser = argparse.ArgumentParser(args)
    parser.add_argument('command', choices=list(FILTERS.keys()),
                        help='filter command to run')
    parser.add_argument('suffix_file', help='path to suffix file')
    parser.add_argument('--invert', action='store_true',
                        help='invert suffix matches')
    parser.add_argument('--in-file', help='input file (defaults to stdin)')
    parser.add_argument('--out-file', help='output file (defaults to stdout)')
    return parser.parse_args()


def process(args):
    suffix_filter = FILTERS[args.command](args.suffix_file, args.invert)
    suffix_filter.process_file(args.in_file, args.out_file)


def main():
    args = parse()
    print(args)
    process(args)


if __name__ == '__main__':
    main()