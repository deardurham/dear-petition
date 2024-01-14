import pytest

from dear_petition.petition.etl.load import link_offense_records, create_documents
from dear_petition.petition.etl.paginator import PAGE_SIZES, OffenseRecordPaginator
from dear_petition.petition.types import dismissed
from dear_petition.petition import constants
from dear_petition.petition.export.forms import AOCFormCR287, AOCFormCR285
from dear_petition.petition.tests.factories import (
    CIPRSRecordFactory,
    OffenseFactory,
    OffenseRecordFactory,
)

pytestmark = pytest.mark.django_db


def many_offense_records(batch, size):
    for i in range(size):
        record = CIPRSRecordFactory(
            batch=batch, jurisdiction=constants.DISTRICT_COURT, county="DURHAM"
        )
        offense = OffenseFactory(
            disposition_method=dismissed.DISMISSED_DISPOSITION_METHODS[0],
            ciprs_record=record,
            jurisdiction=constants.DISTRICT_COURT,
        )
        OffenseRecordFactory(offense=offense, action="CHARGED")


@pytest.fixture
def records_10(batch):
    return many_offense_records(batch=batch, size=10)


@pytest.fixture
def records_11(batch):
    return many_offense_records(batch=batch, size=11)


@pytest.fixture
def records_35(batch):
    return many_offense_records(batch=batch, size=35)


@pytest.fixture
def paginator(petition):
    return petition.get_offense_record_paginator()


@pytest.mark.parametrize("initial_page_size,expected", [[10, 10], [0, 10], [-10, 10]])
def test_paginator_initial_page_size(petition, initial_page_size, expected):
    paginator = OffenseRecordPaginator(petition, initial_page_size=initial_page_size)
    assert paginator.initial_page_size == expected


@pytest.mark.parametrize(
    "form_type,expected",
    [
        [constants.DISMISSED, PAGE_SIZES[constants.DISMISSED]],
        [constants.NOT_GUILTY, PAGE_SIZES[constants.NOT_GUILTY]],
        [constants.UNDERAGED_CONVICTIONS, PAGE_SIZES[constants.UNDERAGED_CONVICTIONS]],
    ],
)
def test_paginator_default_page_size(petition, form_type, expected):
    petition.form_type = form_type
    paginator = OffenseRecordPaginator(petition)
    assert paginator.initial_page_size == expected


@pytest.mark.parametrize(
    "attachment_page_size,expected", [[10, 10], [0, 20], [-10, 20]]
)
def test_paginator_attachment_page_size(petition, attachment_page_size, expected):

    paginator = OffenseRecordPaginator(
        petition, attachment_page_size=attachment_page_size
    )
    assert paginator.attachment_page_size == expected


def test_paginator_petition_offense_records(petition, paginator, records_11):
    link_offense_records(petition)
    assert paginator.petition_offense_records().count() == 10


def test_paginator_attachment_records__10(petition, paginator, records_10):
    link_offense_records(petition)
    # no attachments
    assert not list(paginator.attachment_offense_records())


def test_paginator_attachment_records__11(petition, paginator, records_11):
    link_offense_records(petition)
    records = list(paginator.attachment_offense_records())
    # one attachment
    assert len(records) == 1
    # first attachment has 1 record
    assert records[0].count() == 1


def test_paginator_attachment_records__25(petition, paginator, records_35):
    link_offense_records(petition)
    records = list(paginator.attachment_offense_records())
    # two attachments
    assert len(records) == 2
    # first attachment has 20 records
    assert records[0].count() == 20
    # 2nd attachment has 5 records
    assert records[1].count() == 5


def test_link_offense_records__10(petition, records_10):
    link_offense_records(petition)
    assert petition.offense_records.count() == 10
    assert not petition.has_attachments()


def test_link_offense_records__11(petition, records_11):
    link_offense_records(petition)
    create_documents(petition)
    # one attachment
    assert petition.has_attachments()
    # first attachment has 1 record
    assert petition.documents.order_by("id").last().offense_records.count() == 1


def test_link_offense_records__25(petition, records_35):
    link_offense_records(petition)
    create_documents(petition)
    # two attachments
    assert petition.documents.count() == 3
    attachments = petition.documents.filter(previous_document__isnull=False).order_by(
        "id"
    )
    # first attachment has 20 records
    assert attachments[0].offense_records.count() == 20
    # 2nd attachment has 5 records
    assert attachments[1].offense_records.count() == 5


def test_paginator_same_record_number_order(petition, records_10):
    # get the 10th offense record so we can attach one more offense
    # record to the same CIPRSRecord, so that it crosses the
    # attachment boundary
    charge_1 = petition.get_all_offense_records().last()
    # attach a 2nd dismissed charge
    charge_2 = OffenseRecordFactory(
        offense=OffenseFactory(
            disposition_method=dismissed.DISMISSED_DISPOSITION_METHODS[0],
            ciprs_record=charge_1.offense.ciprs_record,
            jurisdiction=constants.DISTRICT_COURT,
        ),
        action="CHARGED",
    )
    link_offense_records(petition)
    create_documents(petition)
    attachment = (
        petition.documents.filter(previous_document__isnull=False)
        .order_by("pk")
        .first()
    )
    # the 1st charge should always be on the first petition
    assert charge_1.pk in petition.offense_records.values_list("pk", flat=True)
    # the 2nd charge should always be on the attachment
    assert charge_2.pk in attachment.offense_records.values_list("pk", flat=True)


def test_paginator_orders_records_correctly(batch, petition):
    def create_new_ciprs_record(file_no):
        ciprs_record = CIPRSRecordFactory(
            batch=batch,
            file_no=file_no,
            jurisdiction=constants.DISTRICT_COURT,
            county="DURHAM",
        )
        offense = OffenseFactory(
            ciprs_record=ciprs_record,
            jurisdiction=constants.DISTRICT_COURT,
            disposition_method=dismissed.DISMISSED_DISPOSITION_METHODS[0],
        )
        offense_record = OffenseRecordFactory(offense=offense)
        return offense_record.id

    # 11 records total
    id1 = create_new_ciprs_record("99CRAAAAAAAAAAAA")
    id2 = create_new_ciprs_record("00CRBBBBBBBBBBBBB")
    id3 = create_new_ciprs_record("99CRCCCCCCCCCCCC")
    id4 = create_new_ciprs_record("99CRBBBBBBBBBBBB")
    id5 = create_new_ciprs_record("90CRAAAAAAAAAAAA")
    id6 = create_new_ciprs_record("20CRAAAAAAAAAAAA")
    id7 = create_new_ciprs_record("98CRAAAAAAAAAAAA")
    id8 = create_new_ciprs_record("99CRDDDDDDDDDDDD")
    id9 = create_new_ciprs_record("99CRAAAAAAAAAAAA")
    id10 = create_new_ciprs_record("00CRAAAAAAAAAAAA")
    id11 = create_new_ciprs_record("98CRBBBBBBBBBBBB")

    EXPECTED_ORDER_FIRST_FORM = [
        id5,
        id7,
        id11,
        id1,
        id9,
        id4,
        id3,
        id8,
        id10,
        id2,
    ]
    EXPECTED_ORDER_SECOND_FORM = [
        id6,
    ]
    EXPECTED_ORDER_ACROSS_FORMS = EXPECTED_ORDER_FIRST_FORM + EXPECTED_ORDER_SECOND_FORM

    link_offense_records(petition)
    create_documents(petition)
    main_document = petition.base_document
    attachment = petition.documents.filter(previous_document__isnull=False).first()

    main_petition_form = AOCFormCR287(main_document)
    attachment_petition_form = AOCFormCR285(attachment)

    assert (
        list(petition.get_all_offense_records().values_list("id", flat=True))
        == EXPECTED_ORDER_ACROSS_FORMS
    )

    assert (
        list(
            main_petition_form.get_ordered_offense_records().values_list(
                "id", flat=True
            )
        )
        == EXPECTED_ORDER_FIRST_FORM
    )
    assert (
        list(
            attachment_petition_form.get_ordered_offense_records().values_list(
                "id", flat=True
            )
        )
        == EXPECTED_ORDER_SECOND_FORM
    )
