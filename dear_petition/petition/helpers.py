from django.conf import settings

from PIL import ImageFont


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


def get_text_pixel_length(text):
    font = ImageFont.truetype(str(settings.APPS_DIR.path("static/times.ttf")), size=12)
    size = font.getsize(text)
    return size[0]


def get_truncation_point_of_text_by_pixel_size(text, desired_length):
    """
    Given a string and a desired pixel length, will return the index the string needs to be truncated to obtain the the maximal string that can fit within the desired length
    """
    letter_lengths = {}

    def calculate_letter_length(letter):
        if letter in letter_lengths:
            return letter_lengths[letter]
        letter_length = get_text_pixel_length(letter)
        letter_lengths[letter] = letter_length
        return letter_length

    truncated_string_size = 0
    idx = 0
    text_length = len(text)
    while idx < text_length:
        next_letter = text[idx]
        letter_length = calculate_letter_length(next_letter)
        truncated_string_size += letter_length
        if truncated_string_size > desired_length:
            break
        else:
            idx += 1

    return idx
