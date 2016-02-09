"""Parsing Spectramax (quantification) output files.

Not that this ignores most of the file and just grabs the final calculated
quantitation (in ng/ul) for the samples in the measured 384-well plate.
"""

import re

AWKWARD_ENCODING = 'utf-16-le'
BLOCK_DIVIDER = "~End".encode(AWKWARD_ENCODING)
GROUP_ID = "Group: Unknowns".encode(AWKWARD_ENCODING)
BLOCK_END = "Group Summaries".encode(AWKWARD_ENCODING)
OUTSIDE_LADDER = "Range?".encode(AWKWARD_ENCODING)


def parse(fcontents):
    """Parse the file (as a string in fcontents)."""
    # Handle a bunch of Unicode nonsense; files appear to be in UTF-16LE
    quant_results = fcontents.split(BLOCK_DIVIDER)[3]\
        .decode(AWKWARD_ENCODING).encode('ascii', 'ignore').split("\r\n")

    for res in quant_results:
        items = res.split("\t")
        if re.search("\d+", items[0]):  # ignore non-digit rows
            amt = items[9]
            if amt == OUTSIDE_LADDER:
                amt = 100
            yield (int(items[0]), items[1], float(amt))
