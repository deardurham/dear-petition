import re
import typing
from import_export import fields, resources

from dear_petition.petition import constants, models

def parse_agency_full_address(full_address: str) -> typing.Tuple[str, str, str, str, str]:
    """Parse fields needed for agency lookup"""
    [*address_lines, city_state_zip_line] = full_address.split('\n')
    if len(address_lines) == 0:
        raise ValueError("Address must be split into multiple lines")
    adress1 = address_lines[0]
    address2 = address_lines[1] if len(address_lines) == 2 else None

    match = re.match(r'\s*([^,]+?)[,\s]\s*(\w{2})\s*([\w-]+)\s*$', city_state_zip_line)
    if not match:
        raise ValueError("City, State Zipcode format is incorrect")
    (city, state, zipcode) = match.groups()
    return (adress1, address2, city, state, zipcode)


def is_empty_row(row) -> bool:
    return all([value is None for value in row.values()])

class AgencyResource(resources.ModelResource):
    county = fields.Field(attribute='county', column_name='County')
    name = fields.Field(attribute='name', column_name='Arresting Agency')
    address = fields.Field(column_name='Address')

    def init_instance(self, row=None):
        instance = super().init_instance(row)
        if is_empty_row(row):
            return instance
        instance.address1 = row['address1']
        instance.address2 = row['address2']
        return instance

    def get_instance(self, instance_loader, row):
        try:
            return super().get_instance(instance_loader, row)
        except models.Agency.MultipleObjectsReturned as e:
            raise models.Agency.MultipleObjectsReturned(f"There are multiple agencies named '{row['Arresting Agency']}' in county '{row['County']}. Ensure there is only 1.")

    def before_import_row(self, row, **kwargs):
        if is_empty_row(row):
            return

        # found a bug where leading newlines were causing false negative matches for existing agencies
        row['Arresting Agency'] = row['Arresting Agency'].strip()
        row['name'] = row['Arresting Agency']
        row['County'] = row['County'].strip()
        row['county'] = row['County'].strip()

        (address1, address2, city, state, zipcode) = parse_agency_full_address(row['Address'])
        row['city'] = city.strip()
        row['state'] = state.strip()
        row['zipcode'] = zipcode.strip()
        row['address1'] = address1.strip()
        row['address2'] = address2.strip() if address2 else None

        name = row['name']
        if re.search(models.AGENCY_SHERRIFF_OFFICE_PATTERN, name, re.IGNORECASE) or re.search(models.AGENCY_SHERRIFF_DEPARTMENT_PATTERN, name, re.IGNORECASE):
            row['is_sheriff'] = True
        else:
            row['is_sheriff'] = False

    def skip_row(self, instance, original, row, import_validation_errors=None):
        if (is_empty_row(row)):
            return True
        return super().skip_row(instance, original, row, import_validation_errors=import_validation_errors)


    class Meta:
        model = models.Agency
        import_id_fields = ('name', 'county')
        store_instance = True