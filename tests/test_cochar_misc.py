#!/usr/bin/python3
import unittest
from deepdiff import DeepDiff

from randname import randname
from cochar import create_character, get_first_name, get_last_name
from cochar.character import Character
from cochar.utils import ALL_SKILLS
from cochar.error import *

TEST_OCC = {
    "test_occ": {
        "groups": ["edu", "edudex", "edustr", "eduapp", "edupow"],
        "credit_rating": [1, 99],
        "skills": [
            "history",
            "psychology",
            "stealth",
            "listen",
            "psychology",
            [2, "first aid", "mechanical repair", "1l"],
            "2a",
            "2s",
            "2f",
            "2g",
            "2i",
            "2l",
            "2*",
        ],
    }
}


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

    def test_dummy(self):
        self.character.age = 21
        self.assertEqual(self.character.age, 21)

    def test_invalid_sex_value(self):
        with self.assertRaises(InvalidSexValue):
            self.character.sex = "Alien"

    def test_first_name(self):
        self.assertIsInstance(self.character.first_name, str)

    def test_first_name_manually_set(self):
        name = "John"
        c = create_character(self.year, self.country, first_name=name)
        self.assertEqual(c.first_name, name)

    def test_first_name_setter(self):
        name = "@#$%^&*()_+=`~0"
        c = create_character(self.year, self.country, first_name=name)
        c.first_name = name
        self.assertEqual(c.first_name, name)

    def test_first_name_setter_invalid(self):
        with self.assertRaises(EmptyName):
            self.character.first_name = ""

    def test_last_name(self):
        c = create_character(self.year, self.country, last_name="")
        self.assertIsInstance(c.last_name, str)

    def test_last_name_manually_set(self):
        name = "John"
        c = create_character(self.year, self.country, last_name=name)
        self.assertEqual(c.last_name, name)

    def test_last_name_setter(self):
        name = "@#$%^&*()_+=`~0\n|[]{};':\",.<>?"
        c = create_character(self.year, self.country, first_name=name)
        c.last_name = name
        self.assertEqual(c.last_name, name)

    def test_last_name_setter_invalid(self):
        with self.assertRaises(EmptyName):
            self.character.last_name = ""

    def test_year_normal(self):
        self.character.year = 45

    def test_year_not_integer(self):
        with self.assertRaises(InvalidYearValue):
            self.character.year = "a"

    def test_age_normal(self):
        self.character.age = 45

    def test_age_below_range(self):
        with self.assertRaises(AgeNotInRange):
            self.character.age = 14

    def test_age_above_range(self):
        with self.assertRaises(AgeNotInRange):
            self.character.age = 91

    def test_age_not_integer(self):
        with self.assertRaises(InvalidAgeValue):
            self.character.age = "a"

    def test_strength_normal(self):
        self.character.strength = 0

    def test_strength_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.strength = -1

    def test_strength_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.strength = "a"

    def test_condition_normal(self):
        self.character.condition = 0

    def test_condition_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.condition = -1

    def test_condition_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.condition = "a"

    def test_size_normal(self):
        self.character.size = 0

    def test_size_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.size = -1

    def test_size_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.size = "a"

    def test_dexterity_normal(self):
        self.character.dexterity = 0

    def test_dexterity_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.dexterity = -1

    def test_dexterity_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.dexterity = "a"

    def test_appearance_normal(self):
        self.character.appearance = 0

    def test_appearance_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.appearance = -1

    def test_appearance_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.appearance = "a"

    def test_education_normal(self):
        self.character.education = 0

    def test_education_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.education = -1

    def test_education_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.education = "a"

    def test_intelligence_normal(self):
        self.character.intelligence = 0

    def test_intelligence_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.intelligence = -1

    def test_intelligence_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.intelligence = "a"

    def test_power_normal(self):
        self.character.power = 0

    def test_power_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.power = -1

    def test_power_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.power = "a"

    def test_sanity_points_normal(self):
        self.character.sanity_points = 0

    def test_sanity_points_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.sanity_points = -1

    def test_sanity_points_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.sanity_points = "a"

    def test_magic_points_normal(self):
        self.character.magic_points = 0

    def test_magic_points_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.magic_points = -1

    def test_magic_points_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.magic_points = "a"

    def test_hit_points_normal(self):
        self.character.hit_points = 0

    def test_hit_points_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.hit_points = -1

    def test_hit_points_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.hit_points = "a"

    def test_luck_normal(self):
        self.character.luck = 0

    def test_luck_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.luck = -1

    def test_luck_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.luck = "a"

    def test_move_rate_normal(self):
        self.character.move_rate = 0

    def test_move_rate_below_range(self):
        with self.assertRaises(CharacteristicPointsBelowZero):
            self.character.move_rate = -1

    def test_move_rate_not_integer(self):
        with self.assertRaises(CharacteristicValueNotAnInt):
            self.character.move_rate = "a"

    def test_skills_correct(self):
        skills = {"ride": 50, "occult": 50}
        self.character.skills = skills

    def test_skills_incorrect_type(self):
        skills = "ride"
        with self.assertRaises(SkillsNotADict):
            self.character.skills = skills

    def test_skills_value_not_an_int(self):
        skills = {"ride": "a"}
        with self.assertRaises(SkillValueNotAnInt):
            self.character.skills = skills

    # def test_skills_incorrect_key(self):
    #     skills = {"ride": 50, "fake skill": 50}
    #     c = Character()
    #     with self.assertRaises(ValueError):
    #         c.skills = skills

    def test_skills_incorrect_value_below_0(self):
        skills = {"ride": 50, "occult": -1}
        with self.assertRaises(SkillPointsBelowZero):
            self.character.skills = skills

    def test_skills_change_one_skill(self):
        skill = "testing"
        self.character.skills[skill] = 70

    # TODO: Add option of manually setting occupation and hobby points
    # def test_skills_correct_distribution(self):
    #     c = Character(hobby_points=50, occupation_points=0)
    #     # print(c.__dict__)
    #     # print(c)
    #     # print(c.occupation_points, c.hobby_points)
    #     skills_total_sum = sum(list(c.skills.values()))
    #     basic_skills_total_sum = 0
    #     for skill, value in c.skills.items():
    #         if skill == "credit rating":
    #             continue
    #         # assert value == ALL_SKILLS[skill]
    #         basic_skills_total_sum += value
    #         # print(value, ALL_SKILLS[skill])
    #     # basic_skills_total_sum += c.skills['credit rating']
    #     assert skills_total_sum - c.skills["credit rating"] == basic_skills_total_sum
    #     # print(skills_total_sum, basic_skills_total_sum)

    # def test_credit_rating_above_range(self):
    #     c = Character(occupation="lawyer", occupation_points=81)
    #     #  lawyer - credit rating [30, 80]
    #     assert c._occupation_points > c.skills["credit rating"]
    #     # print(c._occupation_points, c.skills["credit rating"])

    # def test_credit_rating_below_min_range(self):
    #     c = Character(occupation="lawyer", occupation_points=29)
    #     #  lawyer - credit rating [30, 80]
    #     assert c._occupation_points >= c.skills["credit rating"]
    #     # print(c._occupation_points, c.skills["credit rating"])

    # def test_credit_rating_below_max_range(self):
    #     c = Character(occupation="lawyer", occupation_points=31)
    #     #  lawyer - credit rating [30, 80]
    #     assert c._occupation_points >= c.skills["credit rating"]
    #     # print(c._occupation_points, c.skills["credit rating"])

    def test_damage_bonus_normal(self):
        self.character.damage_bonus = "+1K4"

    def test_damage_bonus_below_range(self):
        with self.assertRaises(InvalidDamageBonusValue):
            self.character.damage_bonus = -3

    def test_build_normal(self):
        self.character.build = -2
        self.character.build = 2
        self.character.build = 6

    def test_build_below_range(self):
        with self.assertRaises(InvalidBuildValue):
            self.character.build = -3
            self.character.build = -7

    #### OCCUPATIONS ####

    def test_occupation_antiquarian(self):
        occupation = "antiquarian"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_artist(self):
        occupation = "artist"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_athlete(self):
        occupation = "athlete"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_author(self):
        occupation = "author"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_clergy(self):
        occupation = "clergy"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_criminal(self):
        occupation = "criminal"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_dilettante(self):
        occupation = "dilettante"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_doctor_of_medicine(self):
        occupation = "doctor of medicine"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_drifter(self):
        occupation = "drifter"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_engineer(self):
        occupation = "engineer"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_entertainer(self):
        occupation = "entertainer"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_farmer(self):
        occupation = "farmer"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_journalist(self):
        occupation = "journalist"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_lawyer(self):
        occupation = "lawyer"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_librarian(self):
        occupation = "librarian"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_military_officer(self):
        occupation = "military officer"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_missionary(self):
        occupation = "missionary"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_musician(self):
        occupation = "musician"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_parapsychologist(self):
        occupation = "parapsychologist"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_pilot(self):
        occupation = "pilot"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_police_detective(self):
        occupation = "police detective"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_police_officer(self):
        occupation = "police officer"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_private_investigator(self):
        occupation = "private investigator"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_professor(self):
        occupation = "professor"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_soldier(self):
        occupation = "soldier"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_tribe_member(self):
        occupation = "tribe member"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_zealot(self):
        occupation = "zealot"
        c = create_character(self.year, self.country, occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    ########## TEST GENERAL FUNCTIONS ####################

    def test_generate_last_name(self):
        year = 1925
        sex = "M"
        weights = True
        available_sex = ["M", "F", "G", None]
        available_countries = tuple(randname.available_countries())
        for country in available_countries:
            for sex in available_sex:
                name = get_last_name(year, sex, country, weights)
                self.assertIsInstance(name, str)

    def test_generate_first_name(self):
        year = 1925
        sex = "M"
        weights = True
        available_sex = ["M", "F", "G", None]
        available_countries = tuple(randname.available_countries())
        for country in available_countries:
            for sex in available_sex:
                name = get_first_name(year, sex, country, weights)
                self.assertIsInstance(name, str)

    # TEST DUNDER METHODS

    def test_repr_true(self):
        for _ in range(20):
            c = self.character
            d = eval(c.__repr__())
            print(DeepDiff(c.__dict__, d.__dict__), end="")
            assert c == d

    def test_repr_false(self):
        c = self.character
        d = eval(c.__repr__())
        c.occupation = "criminal"
        assert c != d


if __name__ == "__main__":
    unittest.main()
