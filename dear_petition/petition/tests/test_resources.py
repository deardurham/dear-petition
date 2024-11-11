import pytest

from dear_petition.petition.resources import parse_agency_full_address, RecordSummaryResource

pytestmark = pytest.mark.django_db



@pytest.mark.parametrize(
    "full_address, expected_result",
    [
        ("123 Test St.\nWashington, NC 27889", ("123 Test St.", None, "Washington", "NC", "27889")),
        (
            "90 Elk Mountain Road\nAsheville, NC 28804",
            ("90 Elk Mountain Road", None, "Asheville", "NC", "28804"),
        ),
        (
            "16 Fernihurst Drive\nAsheville NC 28801",
            ("16 Fernihurst Drive", None, "Asheville", "NC", "28801"),
        ),
        (
            "P.O. Box 31\n110 N. Church Street # 2\nHertford, NC 27944",
            ("P.O. Box 31", "110 N. Church Street # 2", "Hertford", "NC", "27944"),
        ),
        (
            "450 W. Hanes Mill Road\nWinston-Salem, NC 27894-1666",
            ("450 W. Hanes Mill Road", None, "Winston-Salem", "NC", "27894-1666"),
        ),
    ],
)
def test_parse_agency_full_address(full_address, expected_result):
    parsed_address = parse_agency_full_address(full_address)
    assert parsed_address == expected_result


def test_record_summary_resource(batch, record1, client, dismissed_offense):
    batch.label = "Test Batch"
    batch.save()
    record1.label = "Test Record"
    record1.save()
    batch.client.name = "Test Client"
    batch.client.save()
    resource = RecordSummaryResource()
    dataset = resource.export(batch)

    client_worksheet = dataset.wb.worksheets[0]
    record_worksheet = dataset.wb.worksheets[1]

    assert client_worksheet.title == 'Client Information'
    assert client_worksheet['B1'].value == "Name"
    assert client_worksheet['B2'].value == "Test Client"
    assert record_worksheet.title == "99CRAAAAAAAAAAAA"
    assert record_worksheet['A1'].value == 'Defendent Name'
    assert record_worksheet['A2'].value == 'Test Record'
    assert record_worksheet['B1'].value == 'File No'
    assert record_worksheet['B2'].value == '99CRAAAAAAAAAAAA'
    assert record_worksheet['C1'].value == 'Date Of Birth'
    assert record_worksheet['C2'].value == '1980-07-07'

