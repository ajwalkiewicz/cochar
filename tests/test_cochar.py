import unittest

import cochar
from cochar import character
import cochar.error
import cochar.skill


class TestCharacter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.year = 1925
        cls.country = "US"
        cls.character = cochar.create_character(cls.year, cls.country)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_year_bigger_that_range(self):
        c = cochar.create_character(year=2022, country="US")

    def test_invalid_country(self):
        with self.assertRaises(cochar.error.InvalidCountryValue):
            self.character.country = "T1"

    def test_invalid_occupation_value(self):
        with self.assertRaises(cochar.error.InvalidOccupationValue):
            self.character.occupation = "invalid_occupation"

    def test_points_assignment_to_doge(self):
        TEST_OCC = {
            "test_occ": {
                "groups": ["edu"],
                "credit_rating": [1, 1],
                "skills": [
                    "doge",
                ],
            }
        }
        cochar.OCCUPATIONS_DATA.update(TEST_OCC)
        cochar.OCCUPATIONS_GROUPS[0].append("test_occ")
        cochar.OCCUPATIONS_LIST.append("test_occ")
        occupation = "test_occ"

        character = cochar.create_character(
            self.year, self.country, occupation=occupation
        )

        self.assertGreater(character.doge, character.dexterity)

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
