### Adding new petitions

1. Add the new petition template to dear_petition/static/templates
2. Add to FORM_TYPES constant in dear_petition/petition/constants.py
3. Figure out if the annotations are the same as existing forms (particularly the 287 form which is our default for annotations) or if there are some differences. The get_annotations.py utility is useful for this.
4. Add a class for your form to dear_petition/petition/emport/forms.py
5. Add a new petition type to dear_petition/petition/types
  a. Add a new file with a get_offense_records function
  b. Import file in main.py
  c. Add to TYPE_MAP in main.py
6. In dear_petition/petition/etl/load.py, add to create_batch_petitions function
7. Add to PETITION_FORM_NAMES constant in src/contstants/petitionConstants.js



After you've fully implemented your new petition form, if you find that it is not rendering any of the fields correctly in Google Chrome, try opening the template in Adobe Acrobat Reader and saving it. This will save the FDF file in the correct format that Google can render fields for.