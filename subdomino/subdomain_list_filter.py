"""
Subdomain distribution filter class.
"""


from collections import (
    defaultdict
)


import suffix_filter


class SubdomainListFilter(suffix_filter.SuffixFilter):

    def __init__(self, suffix_file=None, invert=False):
        super().__init__(suffix_file, invert)
        self.subdomain_sets = defaultdict(list)

    def match(self, prefix, suffix, fd):
        labels = prefix.split('.')
        if len(labels) > 1:
            domain = '.'.join([labels[-1], suffix])
            subdomain = labels[-2]
            self.subdomain_sets[domain].append(subdomain)

    def end(self, fd):
        for domain, subdomains in self.subdomain_sets.items():
            print('{}: {}'.format(domain, ', '.join(sorted(subdomains))),
                  file=fd)
