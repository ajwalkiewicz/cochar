import pytest

import cochar


def test_year_bigger_that_range():
    c = cochar.create_character(year=2022, country="US")
    assert c.year == 2022
