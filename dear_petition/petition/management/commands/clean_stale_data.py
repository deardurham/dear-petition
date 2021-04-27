from dear_petition.petition.tasks.clean_stale_data import clean_stale_data


class Command(BaseCommand):
    """
    https://github.com/deardurham/dear-petition/issues/206
    Need to delete data 48 hours after petition is generated to protect the privacy of the clients.
    """

    def handle(self, *args, **options):
        clean_stale_data()
