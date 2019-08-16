import ciprs.reader as reader
import writer
from data_dict import map_data
import json
import argparse

parser = argparse.ArgumentParser(
    description="This will take a court record pdf from CIPRS software and use the data in the pdf to write an expungement petition form pdf."
)
parser.add_argument("input_path", help="The path to the CIPRS court record pdf")
parser.add_argument(
    "template_path",
    help="The path to the empty expungement petition form with field annotations.",
)
parser.add_argument(
    "output_path", help="The path desired for the filled petition form."
)

args = parser.parse_args()

input_path = args.input_path
template_path = args.template_path
output_path = args.output_path

pdf = reader.PDFToTextReader(input_path)
pdf.parse()
json = json.loads(pdf.json())

petition = writer.Writer(json, map_data, template_path, output_path)

petition.get_annotations()
petition.write()
