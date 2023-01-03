def split_first_and_last_name(name):
    names = name.split(" ")

    if len(names) == 1:
        return name, None

    first_name = names[0].capitalize()
    last_name = names[-1].capitalize()
    return first_name, last_name


def get_285_form_agency_address(agency):
    """The 285 box has a giant text box where all the agency information goes"""
    body = ""
    for field_name in [
        "name",
        "address1",
        "address2",
        "city",
        "state",
        "zipcode",
    ]:
        field = getattr(agency, field_name)
        body += f"{field}\n"

    return body
