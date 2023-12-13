import pytest

from dear_petition.petition.resources import parse_agency_full_address

@pytest.mark.parametrize("full_address, expected_result", [
    ('123 Test St.\nWashington, NC 27889', ('123 Test St.', None, 'Washington', 'NC', '27889')),
    ('90 Elk Mountain Road\nAsheville, NC 28804', ('90 Elk Mountain Road', None, 'Asheville', 'NC', '28804')),
    ('16 Fernihurst Drive\nAsheville NC 28801', ('16 Fernihurst Drive', None, 'Asheville', 'NC', '28801')),
    ('P.O. Box 31\n110 N. Church Street # 2\nHertford, NC 27944', ('P.O. Box 31', '110 N. Church Street # 2', 'Hertford', 'NC', '27944')),
    ('450 W. Hanes Mill Road\nWinston-Salem, NC 27894-1666', ('450 W. Hanes Mill Road', None, 'Winston-Salem', 'NC', '27894-1666')),
])
def test_parse_agency_full_address(full_address, expected_result):
    parsed_address = parse_agency_full_address(full_address)
    assert parsed_address == expected_result