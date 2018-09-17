"""
Site filter.
"""


import suffix_filter


class SiteFilter(suffix_filter.SuffixFilter):

    def __init__(self, suffix_file=None, invert=False):
        super().__init__(suffix_file, invert)

    def match(self, prefix, suffix, fd):
        top_level_subdomain = prefix.split('.')[-1]
        print('.'.join([top_level_subdomain, suffix]), fd)
