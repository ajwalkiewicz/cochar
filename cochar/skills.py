"""Skills"""
import random
import os
import json
from collections import UserDict
from typing import Dict, List

from . import errors
from .utils import (
    ALL_SKILLS,
    BASIC_SKILLS,
    CATEGORY_SKILLS,
    CATEGORY_SKILLS_LIST,
    TRANSLATION_DICT,
)
from .settings import *

Skill = Dict[str, int]

# TODO: write unit test
class Skills(UserDict):
    """Dictionary like object to store character's skills.
    Override __setitem__ to validate skills data.

    :param UserDict: UserDict from collections
    :type UserDict: abc.ABCMeta
    """

    # all_skills = ALL_SKILLS.copy()
    def __setitem__(self, key: any, value: int) -> None:
        """Add validation for skill values

        :param key: skill name
        :type key: any
        :param value: skill value
        :type value: int
        :raises SkillValueNotAnInt: when value is not an integer
        :raises SkillPointsBelowZero: when value is less than 0
        """
        key = str(key)
        # if key not in ALL_SKILLS:
        #     raise ValueError(f"Skill: {key}, doesn't exist")
        if not isinstance(value, int):
            raise errors.SkillValueNotAnInt(
                f"Invalid {key.lower()} points. {key.capitalize()} points must be an integer"
            )
        if value < 0:
            raise errors.SkillPointsBelowZero(
                f"{key.capitalize()} points cannot be less than 0"
            )
        # self.all_skills.setdefault()
        self.data[key] = value


# TODO: write unit test
def get_skills(
    occupation: str,
    occupation_points: int,
    hobby_points: int,
    dexterity: int,
    education: int,
    skills: Skills = None,
) -> Skills:
    """Return skills based on:
    occupation, occupation_points, hobby_points, dexterity and education

    If `skills` provided, return `skills`

    Each occupation has related skills, that are chosen randomly. Then
    each skill has randomly assigned skill level - number of points related
    with that skill.

    Dexterity is required for `doge` skill.
    Education is required for `language(own)` skill.

    :param occupation: occupation
    :type occupation: str
    :param occupation_points: occupation_points
    :type occupation_points: int
    :param hobby_points: hobby_points
    :type hobby_points: int
    :param dexterity: dexterity
    :type dexterity: int
    :param education: education
    :type education: int
    :param skills: skills, defaults to None
    :type skills: Skills, optional
    :return: skills with assigned skill level
    :rtype: Skills
    """
    if skills:
        skills = Skills(skills)
    else:
        # Order of following instructions is very important!
        skills: Skills[str, int] = Skills()

        # self.occupation_skills_list: list[str] = []
        # self.hobby_skills_list: list[str] = []

        ALL_SKILLS.update({"doge": dexterity // 2, "language (own)": education})

        # Assigning points to credit rating
        credit_rating_points = get_credit_rating_points(occupation, occupation_points)

        occupation_points_to_distribute = occupation_points - credit_rating_points

        if occupation_points_to_distribute < 0:
            occupation_points_to_distribute = 0

        default_occupations_skills: list = OCCUPATIONS_DATA[occupation]["skills"].copy()
        occupation_skills_list = _get_skills_list(default_occupations_skills)

        # categories = [f"1{cat}" for cat in TRANSLATION_DICT.keys()]
        # hobby_input_list = list(BASIC_SKILLS.keys()) + categories
        default_hobby_skills: list = list(BASIC_SKILLS.keys())
        hobby_skills_list = _get_skills_list(default_hobby_skills)

        skills = _assign_skill_points(occupation_points, occupation_skills_list, skills)
        skills = _assign_skill_points(hobby_points, hobby_skills_list, skills)
        skills = filter_skills(skills)

        skills.setdefault("credit rating", credit_rating_points)

    return skills


# TODO: write unit test
def get_credit_rating_points(occupation: str, occupation_points: int) -> int:
    """For provided occupation, and it occupation points, return
    credit rating points.

    :param occupation: occupation
    :type occupation: str
    :param occupation_points: occupation points
    :type occupation_points: int
    :return: credit rating points
    :rtype: int
    """
    credit_rating_range = OCCUPATIONS_DATA[occupation]["credit_rating"].copy()
    if occupation_points < min(credit_rating_range):
        credit_rating_range = [0, occupation_points]
    if occupation_points < max(credit_rating_range):
        credit_rating_range[1] = occupation_points
    return random.randint(*credit_rating_range)


# TODO: write unit test
def get_skill_points(
    occupation: str,
    education: int,
    power: int,
    dexterity: int,
    appearance: int,
    strength: int,
) -> int:
    """Return skill points based on:
    occupation, education, power, dexterity, appearance and strength.

    Return maximum points for provided occupation.

    :param occupation: occupation name
    :type occupation: str
    :param education: education points
    :type education: int
    :param power: power points
    :type power: int
    :param dexterity: dexterity points
    :type dexterity: int
    :param appearance: appearance points
    :type appearance: int
    :param strength: strength points
    :type strength: int
    :return: skill points
    :rtype: int
    """
    skill_points_groups: tuple[int] = (
        education * 4,  # 1
        education * 2 + power * 2,  # 2
        education * 2 + dexterity * 2,  # 3
        education * 2 + appearance * 2,  # 4
        education * 2 + strength * 2,  # 5
    )
    group_index = [
        index for index, group in enumerate(OCCUPATIONS_GROUPS) if occupation in group
    ]
    points = [skill_points_groups[i] for i in group_index]

    return max(points)


# TODO: write unit test
def _get_skills_list(input_list: list) -> List[str]:
    """Parse an input list taken from `occupation.json` and
    return list of skills

    :param input_list: list of skills from `occupation.json`
    :type input_list: list
    :return: list of skills
    :rtype: List[str]
    """
    skills_list = []
    skills_list += list(
        filter(
            lambda x: len(x) > 2
            and isinstance(x, str)
            and x not in CATEGORY_SKILLS_LIST,
            input_list,
        )
    )
    skills_list += _get_choice_skills(input_list)
    skills_list += _get_category_skills(input_list)
    return skills_list


# TODO: write unit test
def _get_choice_skills(skills_list: list) -> List[str]:
    """Parse a choice option from skills in `occupation.json` and
    return list of skills

    Example:
    [1, "occult", "natural world"] -> ["occult"]
    It means, return randomly one skills from the following options

    :param skills_list: list of skills to choose
    :type skills_list: list
    :return: list of skills
    :rtype: List[str]
    """
    result = []
    for item in skills_list:
        if isinstance(item, tuple):
            population = item[1:]
            k = item[0]
            result.extend(random.choices(population, k=k))
            result.extend(_get_category_skills(result))
            result = list(filter(lambda x: len(x) > 2, result))
    return result


# TODO: write unit test
def _get_category_skills(skills_list: list) -> List[str]:
    """Parse a category skills, and return list of skills.

    Example:
    "1l" -> ["language (german)"]
    It means, one random language from language group.
    "2*" -> ["first aid", "listen"]
    It means, two random skills of all available skills.

    :param skills_list: list of category skill options
    :type skills_list: list
    :return: list of skills
    :rtype: List[str]
    """
    result = []
    for item in skills_list:
        if len(item) == 2:
            k = int(item[0])
            if item[1] == "*":
                population = list(BASIC_SKILLS.keys())
            else:
                population = list(CATEGORY_SKILLS[TRANSLATION_DICT.get(item[1])].keys())
            result.extend(random.choices(population, k=k))

        elif item in CATEGORY_SKILLS_LIST:
            population = list(CATEGORY_SKILLS[item].keys())
            result.extend([random.choice(population)])

    return result


# TODO: write unit test
def _assign_skill_points(points: int, skills_list: list, skills: Skills) -> None:
    """Allocate randomly points to the skills from skills_list
    and store it in Skills object

    :param points: points to allocate
    :type points: int
    :param skills_list: list of skills
    :type skills_list: list
    :param skills: Skills object
    :type skills: Skills
    :return: None
    :rtype: None
    """
    for skill in skills_list:
        if skill in ALL_SKILLS:
            skills.setdefault(skill, ALL_SKILLS[skill])
        else:
            skills.setdefault(skill, 1)

    while points:
        skill = random.choice(skills_list)
        if points <= MAX_SKILL_LEVEL - skills[skill]:
            points_allocation = random.randint(0, points)
        elif sum(list(skills.values())) % 90 == 0:
            break
        elif skills[skill] >= MAX_SKILL_LEVEL:
            continue
        else:
            points_allocation = random.randint(0, MAX_SKILL_LEVEL - skills[skill])
        skills[skill] += points_allocation
        points -= points_allocation

    return skills


# TODO: write unit test
def filter_skills(skills: Dict) -> Dict[str, int]:
    """Filter out all skills with basic value form given dict.

    >>> example_dict = {'psychoanalysis': 1, 'language (spanish)': 66}
    >>> filter_skills(example_dict)
    {'language (spanish)': 66}
    """
    return Skills(
        filter(
            lambda item: ALL_SKILLS.get(item[0], ALL_SKILLS.setdefault(item[0], 1))
            != item[1],
            skills.items(),
        )
    )


# TODO: write unit test
def skill_test(tested_value: int, repetition: int = 1) -> int:
    """Perform skill test.

    Works like improvement test. Roll number between 1 to 100,
    If that number is higher than tested value or higher,
    than 95, then increase tested value with random number,
    between 1 to 10.

    Repeat repetition times.

    .. note:
        for characteristics use `characteristic_test()`

    :param tested_value: tested value
    :type tested_value: int
    :param repetition: how many test to perform
    :type repetition: int
    :return: unchanged, or increased tested value
    :rtype: int
    """
    for _ in range(repetition):
        test = random.randint(1, 100)
        if test > tested_value or test > 95:
            tested_value += random.randint(1, 10)
    return tested_value
