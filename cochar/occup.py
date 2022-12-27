"""**Occupations**
Occupations is a module that contains functions related
with occupations
"""
import copy
import random
from itertools import compress
from typing import List, Tuple

import cochar
import cochar.skill
import cochar.error


def generate_occupation(
    education: int = 1,
    power: int = 1,
    dexterity: int = 1,
    appearance: int = 1,
    strength: int = 1,
    random_mode: bool = False,
    occupation: str = None,
    occup_type: str = None,
    era: List[str] = None,
    tags: List[str] = None,
) -> str:
    """Return occupation based on:
    education, power, dexterity, appearance and strength.

    :param education: education points, defaults to 1
    :type education: int, optional
    :param power: power points, defaults to 1
    :type power: int, optional
    :param dexterity: dexterity points, defaults to 1
    :type dexterity: int, optional
    :param appearance: appearance points, defaults to 1
    :type appearance: int, optional
    :param strength: strength points, defaults to 1
    :type strength: int, optional
    :param random_mode: ignore edu, pow, dex and str points and return totally random occupation, defaults to False
    :type random_mode: bool, optional
    :param occupation: return specified occupation, defaults to None
    :type occupation: str, optional
    :param occup_type: specify type of occupation to return, defaults to None
    :type occup_type: str, optional
    :param era: specify era of occupation to return, defaults to None
    :type era: str, optional
    :param tags: return occupation with defined tags, defaults to None
    :type tags: List[str], optional
    :raises cochar.error.IncorrectOccupation: when occupation is not in the list of available occupations
    :raises cochar.error.NoneOccupationMeetsCriteria: when searching criteria are not met by any occupation
    :return: occupation name
    :rtype: str
    """
    # TODO: What happen if user provide illegal values, strings or below 0?
    skill_points_groups: List[int] = [
        education * 4,  # 1
        education * 2 + power * 2,  # 2
        education * 2 + dexterity * 2,  # 3
        education * 2 + appearance * 2,  # 4
        education * 2 + strength * 2,  # 5
    ]

    if random_mode:
        return random.choice(cochar.OCCUPATIONS_LIST)

    if occupation:
        if occupation not in cochar.OCCUPATIONS_LIST:
            raise cochar.error.IncorrectOccupation(occupation)
        return occupation

    occupation_groups = copy.deepcopy(cochar.OCCUPATIONS_GROUPS)

    if occup_type:
        for i, group in enumerate(occupation_groups):
            occupation_groups[i] = [
                occup
                for occup in group
                if cochar.OCCUPATIONS_DATA[occup]["type"] == occup_type
            ]

    if era:
        for i, group in enumerate(occupation_groups):
            occupation_groups[i] = [
                occup for occup in group if cochar.OCCUPATIONS_DATA[occup]["era"] in era
            ]

    if tags:
        for i, group in enumerate(occupation_groups):
            occupation_groups[i] = [
                occup
                for occup in group
                if set(tags).issubset(set(cochar.OCCUPATIONS_DATA[occup]["tags"]))
            ]

    filtered_occupation_groups = [
        e for e in compress(occupation_groups, occupation_groups)
    ]
    filtered_skill_points_group = [
        e for e in compress(skill_points_groups, occupation_groups)
    ]

    if not filtered_occupation_groups:
        raise cochar.error.NoneOccupationMeetsCriteria(
            f"None occupation meets following criteria: "
            f"type: {occup_type}, era: {era}, tags: {tags}"
        )

    skill_points: int = max(filtered_skill_points_group)
    candidates_for_occupation: List[str] = random.choice(
        [
            group
            for group, points in zip(
                filtered_occupation_groups, filtered_skill_points_group
            )
            if points == skill_points
        ]
    )
    return random.choice(candidates_for_occupation)


def calc_occupation_points(
    occupation: str,
    education: int,
    power: int,
    dexterity: int,
    appearance: int,
    strength: int,
    occupation_points: int = None,
) -> int:
    """Return occupation points based on occupation, education, power,
    dexterity, appearance and strength.

    If ``occupation_points`` provided, return ``occupation_points``

    :param occupation: occupation points
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
    :param occupation_points: occupation points, if provided function returns that value instead of calculating it, defaults to None
    :type occupation_points: int, optional
    :return: occupation points for provided occupation
    :rtype: int
    """
    return (
        occupation_points
        if occupation_points is not None
        else cochar.skill.calc_skill_points(
            occupation, education, power, dexterity, appearance, strength
        )
    )


def calc_hobby_points(intelligence: int, hobby_points: int = None) -> int:
    """Return hobby points, based on intelligence.

    occupation points = 2 * intelligence

    If `hobby_points` provided, return `hobby_points`

    :param intelligence: intelligence points
    :type intelligence: int
    :param hobby_points: hobby_points, defaults to None
    :type hobby_points: int, optional
    :return: hobby points
    :rtype: int
    """
    return hobby_points if hobby_points else intelligence * 2


def get_occupation_list():
    return sorted(cochar.OCCUPATIONS_LIST)
