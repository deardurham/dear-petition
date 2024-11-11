from dear_petition.portal.etl.transform import transform_portal_record


def test_transform_full_record(sample_record):
    expected = {
        "Case Information": {
            "Case Status": "Disposed",
            "Offense Date": "2001-01-01",
            "Arrest Date": "2001-01-03",
        },
        "Defendant": {
            "Name": "DOE, JANE EMMA",
            "Race": "White",
            "Sex": "F",
        },
        "District Court Offense Information": [
            {
                "Disposed On": "2001-12-01",
                "Disposition Method": "District Dismissed by the Court - No Plea Agreement",
                "Records": [
                    {
                        "Count": 1,
                        "Description": "EXTRADITION/FUGITIVE OTH STATE",
                        "Law": "15A-727;733;734",
                        "Severity": "FELONY",
                        "Agency": "Creedmoor Police Department",
                    }
                ],
            }
        ],
        "General": {"County": "Wake", "District": "Yes", "File No": "01CR012345-678"},
        "Superior Court Offense Information": [],
    }
    transformed_record = transform_portal_record(sample_record)
    transformed_record.pop("_meta")
    assert transformed_record == expected
