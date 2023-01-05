import unittest
from unittest.mock import patch

import pytest

import cochar
import cochar.error
import cochar.skill


@pytest.fixture
def year():
    return 1925


@pytest.fixture
def country():
    return "US"


@pytest.mark.parametrize(
    "occupation",
    [
        "antiquarian",
        "artist",
        "athlete",
        "author",
        "bartender",
        "butler/valet",
        "chauffeur",
        "clergy",
        "criminal",
        "dilettante",
        "doctor of medicine",
        "drifter",
        "driver",
        "engineer",
        "entertainer",
        "farmer",
        "gangster boss",
        "hacker",
        "journalist",
        "laborer, unskilled",
        "lawyer",
        "librarian",
        "mechanic",
        "military officer",
        "missionary",
        "musician",
        "nurse",
        "parapsychologist",
        "pilot",
        "police detective",
        "police officer",
        "private investigator",
        "professor",
        "software tester",
        "sailor, commercial",
        "sailor, naval",
        "soldier",
        "tribe member",
        "waiter",
        "zealot",
    ],
)
def test_all_occupations(occupation, year, country):
    c = cochar.create_character(year, country, occupation=occupation)
    assert c.occupation == occupation


@pytest.mark.parametrize("occup_type", ["classic", "expansion"])
def test_create_character_occup_type(year, country, occup_type):
    c = cochar.create_character(year, country, occup_type=occup_type)
    assert cochar.OCCUPATIONS_DATA[c.occupation]["type"] == occup_type


@pytest.mark.parametrize("era", ["classic-1920", "modern"])
def test_create_character_occup_era(year, country, era):
    c = cochar.create_character(year, country, era=era)
    assert cochar.OCCUPATIONS_DATA[c.occupation]["era"] == era


@pytest.mark.parametrize("tags", [["lovecraftian"], ["criminal"]])
def test_create_character_occup_era(year, country, tags):
    c = cochar.create_character(year, country, tags=tags)
    assert cochar.OCCUPATIONS_DATA[c.occupation]["tags"] == tags


# TODO: write better test
@pytest.mark.parametrize(
    "param,value",
    [
        ("first_name", "Adam"),
        ("last_name", "Walkiewicz"),
        ("age", 30),
        ("sex", "M"),
        ("sex", "F"),
        ("occupation", "software tester"),
    ],
)
def test_create_character(param, value):
    assert (
        cochar.create_character(1925, "US", **{param: value}).__getattribute__(param)
        == value
    )


# TODO: improve this test
@pytest.mark.parametrize(
    "year,sex,age,result",
    [
        (1949, "M", 1, 1),
        (1949, "M", 50, 50),
    ],
)
def test_generate_age(year, sex, age, result):
    assert cochar.generate_age(year, sex, age) == result


def test_generate_age_invalid_year():
    with pytest.raises(cochar.error.InvalidYearValue):
        cochar.generate_age("invalid", "F")


# TODO: write better unit test
def test_generate_base_characteristics():
    data = {
        "age": 39,
        "strength": 0,
        "condition": 0,
        "size": 0,
        "dexterity": 0,
        "appearance": 0,
        "education": 0,
        "intelligence": 0,
        "power": 0,
        "luck": 0,
        "move_rate": 0,
    }
    c = cochar.generate_base_characteristics(**data)
    assert 15 <= c[0] <= 90  # strength
    assert 15 <= c[1] <= 90  # condition
    assert 40 <= c[2] <= 90  # size
    assert 15 <= c[3] <= 90  # dexterity
    assert 15 <= c[4] <= 90  # appearance
    assert 40 <= c[5] <= 100  # education, because of characteristics test
    assert 40 <= c[6] <= 90  # intelligence
    assert 15 <= c[7] <= 90  # power
    assert 15 <= c[8] <= 90  # luck
    assert 7 <= c[9] <= 9  # move rate


@pytest.mark.parametrize(
    "power,size,condition,sanity_points,magic_points,hit_points,result",
    [
        (0, 0, 0, 1, 1, 1, (1, 1, 1)),
        (1, 1, 1, 0, 0, 0, (1, 0, 0)),
        (10, 10, 10, 0, 0, 0, (10, 2, 2)),
    ],
)
def test_calc_derived_attributes(
    power, size, condition, sanity_points, magic_points, hit_points, result
):
    assert (
        cochar.calc_derived_attributes(
            power, size, condition, sanity_points, magic_points, hit_points
        )
        == result
    )


@pytest.mark.parametrize("power", [-1, 0, 1, 50])
def test_sanity_points(power):
    assert cochar.calc_sanity_points(power) == power


@pytest.mark.parametrize(
    "power,result",
    [
        (0, 0),
        (4, 0),
        (5, 1),
        (6, 1),
        (60, 12),
    ],
)
def test_calc_magic_points(power, result):
    assert cochar.calc_magic_points(power) == result


@pytest.mark.parametrize(
    "size,condition,result",
    [
        (0, 0, 0),
        (50, 51, 10),
        (50, 50, 10),
        (50, 49, 9),
    ],
)
def test_calc_hit_points(size, condition, result):
    assert cochar.calc_hit_points(size, condition) == result


@pytest.mark.parametrize(
    "strength,size,dexterity,damage_bonus,build,doge,result",
    [
        (0, 0, 0, "+K4", 1, 1, ("+K4", 1, 1)),
        (0, 0, 0, "", 0, 0, ("-2", -2, 0)),
        (62, 62, 50, "", 0, 0, ("0", 0, 25)),
    ],
)
def test_calc_combat_characteristics(
    strength, size, dexterity, damage_bonus, build, doge, result
):
    assert (
        cochar.calc_combat_characteristics(
            strength, size, dexterity, damage_bonus, build, doge
        )
        == result
    )


# TODO: test for bigger ranges
@pytest.mark.parametrize(
    "strength,size,result",
    [
        (0, 0, "-2"),
        (32, 32, "-2"),
        (42, 42, "-1"),
        (62, 62, "0"),
        (82, 82, "+1K4"),
        (102, 102, "+1K6"),
        (200, 83, "+2K6"),
        (300, 64, "+3K6"),
        (400, 44, "+4K6"),
        (500, 24, "+5K6"),
        # (600, 24, "+7K6"),
    ],
)
def test_calc_damage_bonus(strength, size, result):
    assert cochar.calc_damage_bonus(strength, size) == result


# TODO: test for bigger ranges
@pytest.mark.parametrize(
    "strength,size,result",
    [
        (1, 1, -2),
        (32, 32, -2),
        (42, 42, -1),
        (100, 24, 0),
        (100, 64, 1),
        (200, 4, 2),
        (200, 83, 3),
        (300, 64, 4),
        (400, 44, 5),
        (500, 24, 6),
        # (600, 24, 6),
    ],
)
def test_calc_build(strength, size, result):
    assert cochar.calc_build(strength, size) == result


@pytest.mark.parametrize(
    "dexterity,result",
    [
        (49, 24),
        (50, 25),
        (51, 25),
        (0, 0),
    ],
)
def test_calc_doge(dexterity, result):
    assert cochar.calc_doge(dexterity) == result


@pytest.mark.parametrize(
    "characteristic_points,subtract_points,result",
    [
        (50, 10, 40),
        (50, 60, 1),
        (2, 1, 1),
        (0, 0, 1),
        (1, 0, 1),
        (0, -1, 1),
    ],
)
def test_subtract_points_from_characteristic(
    characteristic_points, subtract_points, result
):
    assert (
        cochar.subtract_points_from_characteristic(
            characteristic_points, subtract_points
        )
        == result
    )


@pytest.mark.parametrize(
    "strength,condition,dexterity,subtract_points,result",
    [
        (1, 1, 1, 3, (1, 1, 1)),
        (2, 2, 2, 3, (1, 1, 1)),
        (2, 2, 2, 9, (1, 1, 1)),
    ],
)
def test_subtract_points_from_str_con_dex(
    strength, condition, dexterity, subtract_points, result
):
    assert (
        cochar.subtract_points_from_str_con_dex(
            strength, condition, dexterity, subtract_points
        )
        == result
    )


@pytest.mark.parametrize(
    "tested_value,repetition,result",
    [
        (0, 0, 0),
        (0, 1, 1),
        (1, 1, 1),
        (98, 1, 99),
        (99, 1, 99),
    ],
)
def test_characteristic_test(tested_value, repetition, result):
    if tested_value > 1:

        def mock_random(*args):
            return 100

    else:

        def mock_random(*args):
            return 1

    with patch("random.randint", mock_random):
        assert cochar.characteristic_test(tested_value, repetition) == result


@pytest.mark.parametrize(
    "strength,dexterity,size,result",
    [
        (0, 1, 1, 8),
        (1, 0, 1, 8),
        (0, 0, 1, 7),
        (1, 1, 0, 9),
        (1, 1, 1, 9),
    ],
)
def test_calc_move_rate(strength, dexterity, size, result):
    assert cochar.calc_move_rate(strength, dexterity, size) == result


@pytest.mark.parametrize("input", ["M", "m", "F", "f", None])
def test_generate_sex_valid_input(input):
    assert cochar.generate_sex(input) in ["M", "F"]


@pytest.mark.parametrize("input", ["", False, True])
def test_generate_sex_invalid_input(input):
    with pytest.raises(ValueError):
        cochar.generate_sex(input)


class TestCharacter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.year = 1925
        cls.country = "US"
        cls.character = cochar.create_character(cls.year, cls.country)

    def test_year_bigger_that_range(self):
        cochar.create_character(year=2022, country="US")

    def test_invalid_country(self):
        with self.assertRaises(cochar.error.InvalidCountryValue):
            self.character.country = "T1"

    def test_invalid_occupation_value(self):
        with self.assertRaises(cochar.error.InvalidOccupationValue):
            self.character.occupation = "invalid_occupation"

    def test_points_assignment_to_doge(self):
        # TODO: Create a proper test
        pass
