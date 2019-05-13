import ciprs.reader as reader
import petition.writer as writer
from petition.data_dict import map_data
import json

input_path = '../../cypress-example.pdf'
template_path = '../../petition-template.pdf'
output_path = '../../petition.pdf'

pdf = reader.PDFToTextReader(input_path)
pdf.parse()
json = json.loads(pdf.json())

petition = writer.Writer(json,map_data,template_path,output_path)

petition.get_annotations()
petition.write()


