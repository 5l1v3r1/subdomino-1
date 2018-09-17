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
        self.subdomain_counts = defaultdict(int)

    def match(self, prefix, suffix, fd):
        labels = prefix.split('.')
        if len(labels) > 1:
            subdomain = labels[-2]
            self.subdomain_counts[subdomain] += 1

    def end(self, fd):
        for subdomain, count in self.subdomain_counts.items():
            print('{}: {}'.format(subdomain, count), file=fd)
