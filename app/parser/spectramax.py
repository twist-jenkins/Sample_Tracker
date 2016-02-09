"""Parsing Spectramax (quantification) output files.

Not that this ignores most of the file and just grabs the final calculated
quantitation (in ng/ul) for the samples in the measured 384-well plate.
"""

import re

AWKWARD_ENCODING = 'utf-16-le'
BLOCK_DIVIDER = "~End"
BLOCK_DIVIDER_UTF16 = BLOCK_DIVIDER.encode(AWKWARD_ENCODING)
GROUP_ID = "Group: Unknowns".encode(AWKWARD_ENCODING)
BLOCK_END = "Group Summaries".encode(AWKWARD_ENCODING)
OUTSIDE_LADDER = "Range?".encode(AWKWARD_ENCODING)


def parse(fcontents, utf16=False):
    """Parse the file (as a string in fcontents).

    Note that on disk, these files are written in UTF-16LE but once they
    are stored in a transform spec, they have been converted to UTF-8.
    """  # TODO where does this conversion take place??
    if utf16:
        # Handle a bunch of Unicode nonsense; files appear to be in UTF-16LE
        quant_results = fcontents.split(BLOCK_DIVIDER_UTF16)[3]\
            .decode(AWKWARD_ENCODING).encode('ascii', 'ignore').split("\r\n")
    else:
        quant_results = fcontents.split(BLOCK_DIVIDER)[3].split("\r\n")

    for res in quant_results:
        items = res.split("\t")
        if re.search("\d+", items[0]):  # ignore non-digit rows
            amt = items[9]
            if amt == OUTSIDE_LADDER:
                amt = 100
            yield (int(items[0]), items[1], float(amt))
