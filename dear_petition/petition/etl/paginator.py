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
        self, petition, initial_page_size=None, attachment_page_size=None,
    ):
        self.initial_page_size = initial_page_size or INITIAL_PAGE_SIZE
        self.attachment_page_size = attachment_page_size or ATTACHMENT_PAGE_SIZE
        self.petition = petition
        self.queryset = self.petition.get_all_offense_records()

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
