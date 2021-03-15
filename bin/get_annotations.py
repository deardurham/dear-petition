import sys

import click
import pdfrw


@click.command()
@click.argument("template")
def get_annotations(template):
    """
    This utility prints all the annotations in the provided template.
        template: A path to the template that you would like to get annotations for.
    """

    pdf = pdfrw.PdfReader(template)
    annotations = pdf.pages[0]["/Annots"]
    print("Here is a list of annotations in the document.\n")
    try:
        while True:
            annotation = annotations.pop()
            annotation_name = annotation['/T']
            print(annotation_name)
    except IndexError:
        return

if __name__ == '__main__':
    sys.exit(get_annotations())