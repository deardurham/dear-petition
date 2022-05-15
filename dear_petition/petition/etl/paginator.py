from dear_petition.petition.constants import DISMISSED, ATTACHMENT

INITIAL_PAGE_SIZE = 10
ATTACHMENT_PAGE_SIZE = 20


class OffenseRecordPaginator:
    """
    Class to manage dividing up offense records across petition and petition attachments.
    A petition has attachments if the number of offense records exceeds the available
    rows on the PDF, which in most cases is 10 records.

    Typically:
        * The first 10 offense records are on the petition.
        * Records 11+ are on attachments
        * Each attachment conains up to 20 offense records.
    """

    def __init__(
        self,
        petition,
        initial_page_size=None,
        attachment_page_size=None,
        filter_active=True,
    ):
        self.initial_page_size = (
            abs(initial_page_size)
            if initial_page_size and initial_page_size >= 0
            else INITIAL_PAGE_SIZE
        )
        self.attachment_page_size = (
            abs(attachment_page_size)
            if attachment_page_size and attachment_page_size >= 0
            else ATTACHMENT_PAGE_SIZE
        )
        self.petition = petition
        self.queryset = self.petition.get_all_offense_records(filter_active=True)

    def query(self, start, size):
        """Slice query aginst petition offense records."""
        end = start + size
        return self.queryset[start:end]

    def petition_offense_records(self):
        """
        Return just the offense records for the primary petition,
        usually <= 10 records
        """
        return self.query(start=0, size=self.initial_page_size)

    def attachment_offense_records(self):
        """Generator that returns offense records for each attachment."""
        start = self.initial_page_size
        attachment_records = self.query(start=start, size=self.attachment_page_size)
        while attachment_records.exists():
            yield attachment_records
            start += self.attachment_page_size
            attachment_records = self.query(start=start, size=self.attachment_page_size)
