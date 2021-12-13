import json
import logging
import os
import subprocess
import tempfile

from django.conf import settings
from django.core.files.storage import FileSystemStorage

from ciprs_reader.reader import PDFToTextReader


__all__ = ("transform_ciprs_document", "parse_ciprs_document")


logger = logging.getLogger(__name__)


def transform_ciprs_document(saved_file_path, parser_mode, save_source=settings.CIPRS_READER_SOURCE):
    """Run PDF extraction and return entity-extracted JSON data."""
    reader = PDFToTextReader(saved_file_path, mode=parser_mode)
    try:
        reader.parse(save_source=save_source)
        data = json.loads(reader.json())
    except subprocess.CalledProcessError as e:
        logger.exception(str(e))
        data = {"error": str(e)}
    return data


def parse_ciprs_document(ciprs_document, parser_mode):
    """Save in-memory CIPRS PDF file to temporary location and run PDF extraction."""
    with tempfile.TemporaryDirectory(prefix="ciprs-") as tmp_folder:
        storage = FileSystemStorage(location=tmp_folder)
        storage.save("report.pdf", ciprs_document)
        saved_file_path = os.path.join(storage.location, "report.pdf")
        return transform_ciprs_document(saved_file_path, parser_mode)
