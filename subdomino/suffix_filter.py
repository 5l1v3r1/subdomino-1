"""
Suffix filter base class.
"""

import fileinput
import pygtrie
import sys


class SuffixFilter(object):

    def __init__(self, suffix_file=None, invert=False):
        """
        Constructor.

        Args:
            suffix_file (str): the path to the file containing the suffixes to
                filter.
            invert (bool): whether to invert matches.
        """
        self.suffix_set = pygtrie.CharTrie()
        self.create_filter_set(suffix_file)
        self.invert = invert

    def create_filter_set(self, file_path):
        """
        Add each suffix in a file to the suffix set.

        Args:
            file_path (str): the path to the file containing the suffixes to
                filter.
        """
        for line in fileinput.input(file_path):
            if len(line.strip()) > 0 and line.strip()[:2] != '//':
                self.add_string(line.strip())

    def reset(self):
        """
        Reset the suffix set.
        """
        self.suffix_set = pygtrie.CharTrie()

    def add_string(self, suffix):
        """
        Add a string to the suffix set.

        Args:
            suffix (str): the string to add to the suffix set.
        """
        self.suffix_set[suffix[::-1]] = True

    def filter(self, string):
        """
        Attempt to break an input string into a prefix and suffix in the
        suffix set.

        Args:
            string (str): the string to split.

        Returns:
            A pair (`prefix`, `suffix`) such that if `string` has a suffix
            in the suffix set, then `suffix` is the longest such suffix and
            `prefix` the remainder of the string; if `string` has no such
            suffix, then return the pair (`string`, `None`).
        """
        suffix_match = self.suffix_set.longest_prefix(string[::-1])[0]
        # print('Matched {} to suffix {}'.format(string, suffix_match[::-1]))
        if suffix_match is None:
            return string, None
        else:
            suffix = suffix_match[::-1]
            # Strip off the suffix plus one extra character (a dot) to form
            # the prefix
            prefix = string[:string.rfind(suffix) - 1]
            # print('RETURNING {}, {}'.format(prefix, suffix))
            return prefix, suffix

    def process_string(self, string, fd):
        """
        Check if a string has a suffix in the suffix set and, if it does,
        execute a follow-up function.

        Args:
            string (str): the string to match to a suffix in the set.
            fd (io.TextIOWrapper): the output file (needed for some
                follow-up functions).
        """
        prefix, suffix = self.filter(string)
        if (suffix is not None) ^ self.invert:
            self.match(prefix, suffix, fd)

    def process_file(self, in_file=None, out_file=None):
        with (sys.stdout if out_file is None else open(out_file, 'w')) as fd:
            self.start(fd)
            for line in fileinput.input(in_file):
                self.process_string(line.strip(), fd)
            self.end(fd)

    def match(self, prefix, suffix, fd):
        print('.'.join([prefix, suffix]), file=fd)

    def start(self, fd):
        pass

    def end(self, fd):
        pass
