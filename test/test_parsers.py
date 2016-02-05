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
    res = spectramax.parse(quant_file)
    assert len(res) == 384
    assert res[0][0] == 1
    assert res[383][0] == 384
    assert res[383][1] == 'P24'
    assert res[383][2] == 51.657
