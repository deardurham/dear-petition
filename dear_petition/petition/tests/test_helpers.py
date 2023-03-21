from dear_petition.petition import helpers as ph


def test_get_text_pixel_length():
    text = "This is an example line of text...er...I mean...lorem ipsum?"
    assert ph.get_text_pixel_length(text) == 273


def test_get_truncation_point_of_text_by_pixel_size():
    text = "This is an example line of text...er...I mean...lorem ipsum?"
    truncation_point = ph.get_truncation_point_of_text_by_pixel_size(text, 200)
    assert truncation_point == 42
