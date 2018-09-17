"""
Subdomain distribution filter class.
"""


from collections import (
    defaultdict
)


import suffix_filter


class DistFilter(suffix_filter.SuffixFilter):

    def __init__(self, suffix_file=None, invert=False):
        super().__init__(suffix_file, invert)
        self.subdomain_sets = defaultdict(lambda: defaultdict(int))

    def match(self, prefix, suffix, fd):
        labels = prefix.split('.')
        if len(labels) > 1:
            domain = labels[-1]
            subdomain = labels[-2]
            self.subdomain_sets[domain][subdomain] += 1

    def end(self, fd):
        pass
