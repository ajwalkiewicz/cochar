import unittest
from deepdiff import DeepDiff

from randname import randname
from cochar import create_character, generate_first_name, generate_last_name
from cochar.character import Character
from cochar.utils import ALL_SKILLS
from cochar.error import *


class TestCharacter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.year = 1925
        cls.country = "US"
        cls.character = create_character(cls.year, cls.country)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_year_bigger_that_range(self):
        c = create_character(year=2022, country="US")

    def test_invalid_country(self):
        with self.assertRaises(InvalidCountryValue):
            self.character.country = "T1"

    def test_invalid_occupation_value(self):
        with self.assertRaises(InvalidOccupationValue):
            self.character.occupation = "invalid_occupation"
