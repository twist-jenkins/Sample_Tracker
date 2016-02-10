"""Test import file parsers."""

import pytest
from app.parser import spectramax


@pytest.yield_fixture
def quant_file():
    with open("test/spectramax_example.txt") as sfile:
        yield sfile.read()
    pass


def test_quant_parsing(quant_file):
    """Test parsing of Spectramax quantification output file for 384-well."""
    # Cleanup the file so it is in UTF-8 which is how the backend
    # receives the file from the UI even though the file on disk
    # is encoded in UTF-16LE
    # quant_file = quant_file.decode(spectramax.AWKWARD_ENCODING).encode('ascii', 'ignore')

    res = spectramax.parse(quant_file, utf16=True)
    for conc in res:
        assert len(conc) == 3
        if conc[0] == 1:  # first well
            assert conc[1] == 'A1'
            assert conc[2] == 46.146
        elif conc[0] == 384:
            assert len(conc) == 3
            assert conc[1] == 'P24'
            assert conc[2] == 51.657
