import pytest

from dear_petition.petition.etl.email import extract_username_and_label


@pytest.mark.parametrize(
    "attr,username,label",
    [
        ("user@example.com", "user", ""),
        ("user+mylabel@example.com", "user", "mylabel"),
        ("first.last@example.com", "first.last", ""),
        ("first.last+mylabel@example.com", "first.last", "mylabel"),
    ],
)
def test_extract(attr, username, label):
    extracted_username, extracted_label = extract_username_and_label(attr)
    assert extracted_username == username
    assert extracted_label == label
