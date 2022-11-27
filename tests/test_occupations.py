#!/usr/bin/python3
import pytest

import cochar
import cochar.occup
import cochar.error


def test_get_occupation_list():
    assert set(cochar.occup.get_occupation_list()) == set(cochar.OCCUPATIONS_LIST)


def test_get_hobby_points():
    points = cochar.occup.calc_hobby_points(50)
    assert points == 100


def test_generate_occupation_random():
    o = cochar.occup.generate_occupation(random_mode=True)
    assert o in cochar.OCCUPATIONS_LIST


def test_generate_occupation_with_occupation():
    occupation = cochar.occup.generate_occupation(occupation="criminal")
    assert occupation == "criminal"


def test_generate_occupation_tags():
    occupation = cochar.occup.generate_occupation(tags=["criminal"])
    assert occupation in ["gangster boss", "criminal"]
    assert occupation not in ["drifter"]


def test_generate_occupation_occup_type():
    o = cochar.occup.generate_occupation(occup_type="custom")
    assert o == "software tester"


def test_generate_occupation_era():
    o = cochar.occup.generate_occupation(era="modern", occup_type="custom")
    # TODO: improve in future, when there will be more modern occupation than just one
    assert o == "software tester"


def test_generate_occupation_value_error():
    with pytest.raises(cochar.error.NoneOccupationMeetsCriteria):
        cochar.occup.generate_occupation(era="modern", tags=["lovecraftian"])
