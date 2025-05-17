import pathlib
import json

from bs4 import BeautifulSoup
import pytest


@pytest.fixture(scope="module")
def sample_record():
    path = pathlib.Path(__file__).parent / "data" / "record.html"
    return path.read_text()


@pytest.fixture(scope="module")
def soup(sample_record):
    return BeautifulSoup(sample_record, features="html.parser")


@pytest.fixture(scope="module")
def dispositions():
    path = pathlib.Path(__file__).parent / "data" / "dispositions.json"
    return json.loads(path.read_text())
