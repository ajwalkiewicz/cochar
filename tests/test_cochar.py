import unittest

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


class TestCharacter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.year = 1925
        cls.country = "US"
        cls.character = cochar.create_character(cls.year, cls.country)

    def test_year_bigger_that_range(self):
        c = cochar.create_character(year=2022, country="US")

    def test_invalid_country(self):
        with self.assertRaises(cochar.error.InvalidCountryValue):
            self.character.country = "T1"

    def test_invalid_occupation_value(self):
        with self.assertRaises(cochar.error.InvalidOccupationValue):
            self.character.occupation = "invalid_occupation"

    def test_points_assignment_to_doge(self):
        # TODO: Create a proper test
        pass

    def test_sanity_points(self):
        power = 100
        sanity_points = cochar.calc_sanity_points(power)
        self.assertEqual(sanity_points, power)

    def test_calc_magic_points(self):
        power = 100
        magic_points = cochar.calc_magic_points(power)
        self.assertEqual(magic_points, 20)

    def test_calc_hit_points(self):
        size = 50
        condition = 50
        hit_points = cochar.calc_hit_points(size, condition)
        self.assertEqual(hit_points, 10)

    def test_calc_damage_bonus(self):
        # TODO: test for bigger ranges
        self.assertEqual(cochar.calc_damage_bonus(0, 0), "-2")
        self.assertEqual(cochar.calc_damage_bonus(32, 32), "-2")
        self.assertEqual(cochar.calc_damage_bonus(42, 42), "-1")
        self.assertEqual(cochar.calc_damage_bonus(62, 62), "0")
        self.assertEqual(cochar.calc_damage_bonus(82, 82), "+1K4")
        self.assertEqual(cochar.calc_damage_bonus(102, 102), "+1K6")
        self.assertEqual(cochar.calc_damage_bonus(200, 83), "+2K6")
        self.assertEqual(cochar.calc_damage_bonus(300, 64), "+3K6")
        self.assertEqual(cochar.calc_damage_bonus(400, 44), "+4K6")
        self.assertEqual(cochar.calc_damage_bonus(500, 24), "+5K6")
        # self.assertEqual(cochar.calc_damage_bonus(600, 24), "+7K6")

    def test_calc_build(self):
        # TODO: test for bigger ranges
        self.assertEqual(cochar.calc_build(1, 1), -2)
        self.assertEqual(cochar.calc_build(32, 32), -2)
        self.assertEqual(cochar.calc_build(42, 42), -1)
        self.assertEqual(cochar.calc_build(100, 24), 0)
        self.assertEqual(cochar.calc_build(100, 64), 1)
        self.assertEqual(cochar.calc_build(200, 4), 2)
        self.assertEqual(cochar.calc_build(200, 83), 3)
        self.assertEqual(cochar.calc_build(300, 64), 4)
        self.assertEqual(cochar.calc_build(400, 44), 5)
        self.assertEqual(cochar.calc_build(500, 24), 6)
        # self.assertEqual(cochar.calc_build(600, 24), 6)

    def test_calc_doge(self):
        self.assertEqual(cochar.calc_doge(51), 25)
