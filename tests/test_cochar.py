#!/usr/bin/python3
import unittest

import random
from randname import randname
from cochar import Character
from unittest.mock import patch

class TestCharacter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.character = Character()

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_dummy(self):
        char = Character()
        char.age = 21
        self.assertEqual(char.age, 21)

    def test_general_wrong_things(self):
        c = Character(
            # year="first",
            # age="1",
            first_name="",
            last_name="",
            # country="San Escobar",
            # occupation="not optima",
            # occupation_points="twelfe",
            # hobby_points="milion",
            # characteristics="Nothing",
            # luck="a lot",
            # skills="Chuck Norris",
            # combat_values={"hello": "world"},
            weights=5
        )

        with self.assertRaises(ValueError):
            c = Character(sex="Ass",)

    def test_first_name(self):
        c = Character(first_name="")
        self.assertIsInstance(c.first_name, str)

    def test_first_name_manually_set(self):
        name = "John"
        c = Character(first_name=name)
        self.assertEqual(c.first_name, name)

    def test_first_name_setter(self):
        name = "@#$%^&*()_+=`~0"
        c = Character()
        c.first_name = name
        self.assertEqual(c.first_name, name)

    def test_first_name_setter_invalid(self):
        c = Character()
        with self.assertRaises(ValueError):
            c.first_name = ""

    def test_last_name(self):
        c = Character(last_name="")
        self.assertIsInstance(c.last_name, str)

    def test_last_name_manually_set(self):
        name = "John"
        c = Character(last_name=name)
        self.assertEqual(c.last_name, name)

    def test_last_name_setter(self):
        name = "@#$%^&*()_+=`~0\n|[]{};':\",.<>?"
        c = Character()
        c.last_name = name
        self.assertEqual(c.last_name, name)

    def test_last_name_setter_invalid(self):
        c = Character()
        with self.assertRaises(ValueError):
            c.last_name = ""

    def test_year_normal(self):
        self.character.year = 45

    def test_year_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.year = "a"   
   
    def test_age_normal(self):
        self.character.age = 45

    def test_age_below_range(self):
        with self.assertRaises(ValueError):
            self.character.age = 14

    def test_age_above_range(self):
        with self.assertRaises(ValueError):
            self.character.age = 91

    def test_age_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.age = "a"    

    def test_strength_normal(self):
        self.character.strength = 0

    def test_strength_below_range(self):
        with self.assertRaises(ValueError):
            self.character.strength = -1

    def test_strength_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.strength = "a"

    def test_condition_normal(self):
        self.character.condition = 0

    def test_condition_below_range(self):
        with self.assertRaises(ValueError):
            self.character.condition = -1

    def test_condition_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.condition = "a"

    def test_size_normal(self):
        self.character.size = 0

    def test_size_below_range(self):
        with self.assertRaises(ValueError):
            self.character.size = -1

    def test_size_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.size = "a"

    def test_dexterity_normal(self):
        self.character.dexterity = 0

    def test_dexterity_below_range(self):
        with self.assertRaises(ValueError):
            self.character.dexterity = -1

    def test_dexterity_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.dexterity = "a"

    def test_apperance_normal(self):
        self.character.apperance = 0

    def test_apperance_below_range(self):
        with self.assertRaises(ValueError):
            self.character.apperance = -1

    def test_apperance_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.apperance = "a"

    def test_edducation_normal(self):
        self.character.edducation = 0

    def test_edducation_below_range(self):
        with self.assertRaises(ValueError):
            self.character.edducation = -1

    def test_edducation_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.edducation = "a"

    def test_intelligence_normal(self):
        self.character.intelligence = 0

    def test_intelligence_below_range(self):
        with self.assertRaises(ValueError):
            self.character.intelligence = -1

    def test_intelligence_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.intelligence = "a"

    def test_power_normal(self):
        self.character.power = 0

    def test_power_below_range(self):
        with self.assertRaises(ValueError):
            self.character.power = -1

    def test_power_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.power = "a"
    
    def test_sanity_points_normal(self):
        self.character.sanity_points = 0

    def test_sanity_points_below_range(self):
        with self.assertRaises(ValueError):
            self.character.sanity_points = -1

    def test_sanity_points_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.sanity_points = "a"

    def test_magic_points_normal(self):
        self.character.magic_points = 0

    def test_magic_points_below_range(self):
        with self.assertRaises(ValueError):
            self.character.magic_points = -1

    def test_magic_points_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.magic_points = "a"
    
    def test_hit_points_normal(self):
        self.character.hit_points = 0

    def test_hit_points_below_range(self):
        with self.assertRaises(ValueError):
            self.character.hit_points = -1

    def test_hit_points_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.hit_points = "a"

    def test_luck_normal(self):
        self.character.luck = 0

    def test_luck_below_range(self):
        with self.assertRaises(ValueError):
            self.character.luck = -1

    def test_luck_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.luck = "a"

    def test_move_rate_normal(self):
        self.character.move_rate = 0

    def test_move_rate_below_range(self):
        with self.assertRaises(ValueError):
            self.character.move_rate = -1

    def test_move_rate_not_integer(self):
        with self.assertRaises(ValueError):
            self.character.move_rate = "a"

    def test_skills_correct(self):
        skills = {"ride": 50, "occult": 50}
        c = Character()
        c.skills = skills

    def test_skills_incorrect_type(self):
        skills = "ride"
        c = Character()
        with self.assertRaises(ValueError):
            c.skills = skills

    # def test_skills_incorrect_key(self):
    #     skills = {"ride": 50, "fake skill": 50}
    #     c = Character()
    #     with self.assertRaises(ValueError):
    #         c.skills = skills

    def test_skills_incorrect_value_below_0(self):
        skills = {"ride": 50, "occult": -1}
        c = Character()
        with self.assertRaises(ValueError):
            c.skills = skills

    def test_skills_change_one_skill(self):
        skill = "testing"
        self.character.skills[skill] = 70

    def test_damage_bonus_normal(self):
        self.character.damage_bonus = "+1K4"

    def test_damage_bonus_below_range(self):
        with self.assertRaises(ValueError):
            self.character.damage_bonus = -3

    def test_build_normal(self):
        self.character.build = -2
        self.character.build = 2
        self.character.build = 6

    def test_build_below_range(self):
        with self.assertRaises(ValueError):
            self.character.build = -3
            self.character.build = -7

#### OCCUPATIONS ####

    def test_occupation_antiquarian(self):
        occupation = "antiquarian"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_artist(self):
        occupation = "artist"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_athlete(self):
        occupation = "athlete"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_author(self):
        occupation = "author"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_clergy(self):
        occupation = "clergy"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_criminal(self):
        occupation = "criminal"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_dilettante(self):
        occupation = "dilettante"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_doctor_of_medicine(self):
        occupation = "doctor of medicine"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_drifter(self):
        occupation = "drifter"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_engineer(self):
        occupation = "engineer"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_entertainer(self):
        occupation = "entertainer"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_farmer(self):
        occupation = "farmer"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_journalist(self):
        occupation = "journalist"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_lawyer(self):
        occupation = "lawyer"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_librarian(self):
        occupation = "librarian"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_military_officer(self):
        occupation = "military officer"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_missionary(self):
        occupation = "missionary"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_musician(self):
        occupation = "musician"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_parapsychologist(self):
        occupation = "parapsychologist"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_pilot(self):
        occupation = "pilot"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_police_detective(self):
        occupation = "police detective"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_police_officer(self):
        occupation = "police officer"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_private_investigator(self):
        occupation = "private investigator"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_professor(self):
        occupation = "professor"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_soldier(self):
        occupation = "soldier"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_tribe_member(self):
        occupation = "tribe member"
        c = Character(occupation=occupation)
        self.assertEqual(c.occupation, occupation)

    def test_occupation_zealot(self):
        occupation = "zealot"
        c = Character(occupation=occupation) 
        self.assertEqual(c.occupation, occupation)

########## TEST GENERAL FUNCTIONS ####################

    def test_generate_last_name(self):
        year = 1925
        sex = 'M'
        weights = True
        available_sex = ['M', 'F', 'G', None]
        available_countries = tuple(randname.available_countries())
        for country in available_countries:
            for sex in available_sex:
                name = Character.generate_last_name(year, sex, country, weights)
                self.assertIsInstance(name, str)

    def test_generate_first_name(self):
        year = 1925
        sex = 'M'
        weights = True
        available_sex = ['M', 'F', 'G', None]
        available_countries = tuple(randname.available_countries())
        for country in available_countries:
            for sex in available_sex:
                name = Character.generate_first_name(year, sex, country, weights)
                self.assertIsInstance(name, str)


########## TEST DUNDER METHODS ####################

    def test_repr_true(self):
        c = Character()
        d = eval(c.__repr__())
        assert c == d

    def test_repr_false(self):
        c = Character(occupation="artist")
        d = eval(c.__repr__())
        c.occupation = "criminal"
        assert c != d


if __name__ == "__main__":
    unittest.main()
