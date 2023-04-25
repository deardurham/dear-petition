from dear_petition.petition import helpers as ph


def test_get_text_pixel_length():
    text = "m"
    assert ph.get_text_pixel_length(text) == 10


def test_get_truncation_point_of_text_by_pixel_size():
    text = "This is an example line of text...er...I mean...lorem ipsum?"
    truncation_point = ph.get_truncation_point_of_text_by_pixel_size(text, 200)
    assert truncation_point == 42


def test_get_truncation_point_of_short_text_by_pixel_size():
    """When the full text is shorter than the desired truncation point, it should just return the whole string."""
    text = "Lorem ipsum"
    truncation_point = ph.get_truncation_point_of_text_by_pixel_size(text, 20000)
    assert truncation_point == len(text)
