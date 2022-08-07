"""Characters"""
from distutils.command.build import build
import random
import json
import os
import logging

from bisect import bisect_left
from typing import List, Union, Tuple

import randname

from .character import Character, get_sex
from .occupations import get_occupation, get_occupation_points, get_hobby_points
from .skills import Skills, get_skills
from . import errors
from .utils import (
    AGE_RANGE,
    YEAR_RANGE,
)
from .settings import *


def create_character(
    year: int,
    country: str,
    first_name: str = "",
    last_name: str = "",
    age: int = False,
    sex: str = False,
    occupation: str = "optimal",
    skills: Skills = {},
) -> Character:
    """Create character
    Use this function instead of instantiating Character class

    :param year: year of the game
    :type year: int
    :param country: country where character lives
    :type country: str
    :param first_name: character first name
    :type first_name: str
    :param last_name: character last name
    :type last_name: str
    :param age: character  age
    :type age: int
    :param sex: character sex
    :type sex: int
    :param occupation: character occupation
    :type occupation: str
    :param skills: character skills
    :type skills: Skills
    :return: character object
    :rtype: Character
    """
    weights = WEIGHTS

    if sex in SEX_OPTIONS:
        sex = get_sex(sex)
    else:
        raise ValueError(f"incorrect sex value: {sex} -> ['M', 'F', None']")

    age: int = get_age(year, sex, age)

    if first_name == "":
        first_name: str = (
            get_first_name(year, sex, country, weights) if not first_name else first_name
        )
    else:
        first_name = first_name
        
    if last_name == "":    
        last_name: str = (
            get_last_name(year, sex, country, weights) if not last_name else last_name
        )
    else:
        last_name = last_name

    (
        strength,
        condition,
        size,
        dexterity,
        appearance,
        education,
        intelligence,
        power,
        luck,
        move_rate,
    ) = get_base_characteristics(age=age)

    occupation = get_occupation(
        education=education,
        power=power,
        dexterity=dexterity,
        appearance=appearance,
        strength=strength,
        occupation=occupation,
    )

    sanity_points, magic_points, hit_points = get_derived_attributes(
        power, size, condition
    )

    damage_bonus, build, doge = get_combat_characteristics(strength, size, dexterity)

    occupation_points = get_occupation_points(
        occupation, education, power, dexterity, appearance, strength
    )
    hobby_points = get_hobby_points(intelligence)
    skills = get_skills(
        occupation, occupation_points, hobby_points, dexterity, education
    )

    return Character(
        year=year,
        country=country,
        first_name=first_name,
        last_name=last_name,
        age=age,
        sex=sex,
        occupation=occupation,
        strength=strength,
        condition=condition,
        size=size,
        dexterity=dexterity,
        appearance=appearance,
        education=education,
        intelligence=intelligence,
        power=power,
        luck=luck,
        damage_bonus=damage_bonus,
        build=build,
        move_rate=move_rate,
        skills=skills,
        doge=doge,
        sanity_points=sanity_points,
        magic_points=magic_points,
        hit_points=hit_points,
    )


def get_age(year, sex, age: int = False) -> int:
    """Set age

    :param age: new age, defaults to None
    :type age: int, optional
    :return: new age
    :rtype: int
    """
    if age is False:
        variable_year = year
        if variable_year < 1950:
            variable_year = 1950
        else:
            year_index = bisect_left(YEAR_RANGE, year)
            variable_year = YEAR_RANGE[year_index]
        variable_name = f"pop{variable_year}"

        with open(POP_PYRAMID_PATH) as json_file:
            age_population = AGE_RANGE
            age_weights = json.load(json_file)[variable_name][sex][3:-1]
            age_range = random.choices(age_population, weights=age_weights)[0]
            age = random.randint(*age_range)

    return age


def get_base_characteristics(
    age,
    strength: int = 0,
    condition: int = 0,
    size: int = 0,
    dexterity: int = 0,
    appearance: int = 0,
    education: int = 0,
    intelligence: int = 0,
    power: int = 0,
    move_rate: int = 0,
    luck: int = 0,
) -> tuple:
    if strength == 0:
        strength = random.randint(15, 90)
    if condition == 0:
        condition = random.randint(15, 90)
    if size == 0:
        size = random.randint(40, 90)
    if dexterity == 0:
        dexterity = random.randint(15, 90)
    if appearance == 0:
        appearance = random.randint(15, 90)
    if education == 0:
        education = random.randint(40, 90)
    if intelligence == 0:
        intelligence = random.randint(40, 90)
    if power == 0:
        power = random.randint(15, 90)
    if move_rate == 0:
        move_rate = 0
    if luck == 0:
        luck = random.randint(15, 90)
    if age <= 19:
        luck = max(luck, random.randint(15, 90))

    age_range = bisect_left(MODIFIERS["age_range"], age)
    mod_char_points = MODIFIERS["mod_char_points"][age_range]
    mod_app = MODIFIERS["mod_app"][age_range]
    mod_move_rate = MODIFIERS["mod_move_rate"][age_range]
    mod_edu = MODIFIERS["mod_edu"][age_range]

    appearance = subtract_points_from_characteristic(appearance, mod_app)
    strength, condition, dexterity = _subtract_points_from_str_con_dex(
        strength, condition, dexterity, mod_char_points
    )
    education = test_characteristic(education, mod_edu)
    move_rate = get_move_rate(strength, dexterity, size) - mod_move_rate

    return (
        strength,
        condition,
        size,
        dexterity,
        appearance,
        education,
        intelligence,
        power,
        luck,
        move_rate,
    )


def get_derived_attributes(
    power: int,
    size: int,
    condition: int,
    sanity_points: int = 0,
    magic_points: int = 0,
    hit_points: int = 0,
) -> Tuple[int, int, int]:
    """Based on power, size and condition,
    return sanity, magic and hit points

    :param power: power points
    :type power: int
    :param size: size points
    :type size: int
    :param condition: condition points
    :type condition: int
    :param sanity_points: sanity points, defaults to 0
    :type sanity_points: int, optional
    :param magic_points: magic points, defaults to 0
    :type magic_points: int, optional
    :param hit_points: hit points, defaults to 0
    :type hit_points: int, optional
    :return: (sanity points, magic points, hit points)
    :rtype: tuple
    """
    if sanity_points == 0:
        sanity_points = power
    if magic_points == 0:
        magic_points = power // 5
    if hit_points == 0:
        hit_points = (size + condition) // 10

    return sanity_points, magic_points, hit_points


def get_combat_characteristics(
    strength: int, size: int, dexterity: int, skills: Skills = None
) -> Tuple[str, int, int]:
    """_summary_

    :param strength: strength points
    :type strength: int
    :param size: size points
    :type size: int
    :param dexterity: dexterity points
    :type dexterity: int
    :param skills: Skills dictionary, defaults to None
    :type skills: Skills, optional
    :raises ValueError: raise if skills is not an instance of Skills
    :return: (damage bonus, build, doge)
    :rtype: Tuple(str, int, int)
    """
    # TODO: Investigate: why am I using Skills here?
    if not skills:
        skills = Skills({})
    if not isinstance(skills, Skills):
        raise ValueError()

    damage_bonus = get_damage_bonus(strength, size)
    build = get_build(strength, size)
    doge = get_doge(dexterity, skills)

    return damage_bonus, build, doge


def get_damage_bonus(strength: int, size: int) -> str:
    """Set character damage bonus.

    Use current Character object state to set its damage bonus.

    :return: damage bonus
    :rtype: str
    """
    VALUE_MATRIX = {
        "combat_range": [64, 84, 124, 164, 204, 283, 364, 444, 524],
        "damage_bonus": [
            "-2",
            "-1",
            "0",
            "+1K4",
            "+1K6",
            "+2K6",
            "+3K6",
            "+4K6",
            "+5K6",
        ],
    }
    sum_str_siz = strength + size
    combat_range = bisect_left(VALUE_MATRIX["combat_range"], sum_str_siz)
    damage_bonus = VALUE_MATRIX["damage_bonus"][combat_range]
    return damage_bonus


def get_build(strength: int, size: int) -> int:
    """Set character build

    Use current character object state to set its build.

    :return: build
    :rtype: int
    """
    sum_str_siz = strength + size
    combat_range = bisect_left(VALUE_MATRIX["combat_range"], sum_str_siz)
    build = VALUE_MATRIX["build"][combat_range]
    return build


def get_doge(dexterity: int, skills: Skills = None) -> int:
    """Set character doge.

    Use current character object state to set its doge value.

    .. warning::

        When used outside ``__init__`` may require to set first
        ``self.skills['doge']``. Use ``self.doge`` to manually set doge instead of
        this function.

    .. note::

        Just a note.

    :return: doge
    :rtype: int
    """
    if "doge" in skills:
        doge = skills["doge"]
    else:
        doge = dexterity // 2
    return doge


def subtract_points_from_characteristic(
    characteristic_points: int, subtract_points: int
) -> int:
    return (
        characteristic_points - subtract_points
        if characteristic_points > subtract_points
        else 1
    )


def _subtract_points_from_str_con_dex(
    strength: int, condition: int, dexterity: int, subtract_points: int
) -> Tuple[int, int, int]:
    strength = strength
    condition = condition
    dexterity = dexterity
    for _ in range(subtract_points):
        characteristic_to_subtract = [
            characteristic
            for characteristic in (strength, condition, dexterity)
            if characteristic != 1
        ]
        if characteristic_to_subtract:
            characteristic = random.choice(characteristic_to_subtract)
            characteristic = characteristic - 1
        else:
            break

    return strength, condition, dexterity


def test_characteristic(skill_value: str, repetition: int) -> int:
    for _ in range(repetition):
        test = random.randint(1, 100)
        if skill_value < test:
            skill_value += random.randint(1, 10)
    return skill_value


def get_move_rate(strength: int, dexterity: int, size: int) -> None:
    if dexterity < size and strength < size:
        move_rate = 7
    elif strength >= size and dexterity >= size:
        move_rate = 9
    else:
        move_rate = 8

    return move_rate


# TODO: How to combine return and raise in one function
def is_skill_valid(skill_value: int, skill_name: str) -> bool:
    """Check if skill value is int type and it is not
    below 0.

    :param new_variable: variable to check
    :type new_variable: int
    :param variable_name: name of that variable
    :type variable_name: str
    :raises SkillValueNotAnInt: if variable is not an integer
    :raises SkillValueNotAnInt: if variable is below 0

    >>> Character._Character__validate_character_properties("a", 'luck')
    errors.SkillValueNotAnInt: Invalid luck points. Luck points must be an integer
    >>> Character._Character__validate_character_properties(-1, 'luck')
    errors.SkillValueNotAnInt: Luck points cannot be less than 0
    """
    skill_name = str(skill_name)

    if not isinstance(skill_value, int):
        raise errors.SkillValueNotAnInt(
            f"Invalid {skill_name.lower()} points. {skill_name.capitalize()} points must be an integer"
        )
    if skill_value < 0:
        raise ValueError(f"{skill_name.capitalize()} points cannot be less than 0")

    return True


def get_last_name(year: int, sex: str, country: str, weights: bool) -> str:
    """Generate Last Name.
    Return random last name for the given parameters
    This method is not recommended as it initialize a Character() class.
    For faster generation use module randname

    :param year: year of the data set with names (if data set not available use a closes available data set)
    :type year: int
    :param sex: name gender, available options ['M', 'F', 'N', None]
    :type sex: str
    :param country: name country
    :type country: str
    :param weights: If true, take under account popularity of names. [default: True]
    :type weights: bool
    :return: last name
    :rtype: str
    """
    sex = get_valid_sex(sex, country, name="last_names")
    return randname.last_name(
        year, sex, country, weights, database=DATABASE, show_warnings=SHOW_WARNINGS
    )


def get_first_name(year: int, sex: str, country: str, weights: bool) -> str:
    """Generate First Name.
    Return random first name for the given parameters
    This method is not recommended as it initialize a Character() class.
    For faster generation use module randname

    :param year: year of the data set with names (if data set not available use a closes available data set)
    :type year: int
    :param sex: name gender, available options ['M', 'F', 'N', None]
    :type sex: str
    :param country: name country
    :type country: str
    :param weights: if true, take under account popularity of names. [default: True]
    :type weights: bool
    :return: first name
    :rtype: str
    """
    sex = get_valid_sex(sex, country, name="first_names")
    return randname.first_name(
        year, sex, country, weights, database=DATABASE, show_warnings=SHOW_WARNINGS
    )


def get_valid_sex(sex: str, country: str, name: str) -> str:
    available_sex = randname.data_lookup()[country][name]
    if sex not in available_sex:
        if "N" in available_sex:
            sex = "N"
        else:
            sex = random.choice(available_sex)
    return sex


if __name__ == "__main__":
    import doctest

    doctest.testmod()
