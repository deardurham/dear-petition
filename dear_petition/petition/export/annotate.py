"""Helpers to prepare context for pdfrw templates."""

__all__ = ("Checkbox", "add_pdf_template_annotations")


class Checkbox(str):
    annotation = "AS"


def add_pdf_template_annotations(data):
    for key, value in data.items():
        annotation = "V"
        if hasattr(value, "annotation"):
            annotation = value.annotation
        data[key] = {annotation: value}
