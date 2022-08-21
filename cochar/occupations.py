"""Errors"""
import random
import os
import json
from typing import List, Tuple

from .skills import get_skill_points
from .settings import OCCUPATIONS_LIST, OCCUPATIONS_GROUPS

# TODO: write unit test
def get_occupation(
    education: int,
    power: int,
    dexterity: int,
    appearance: int,
    strength: int,
    occupation: str = "optimal",
) -> str:
    """Return occupation based on:
    education, power, dexterity, appearance and strength

    :param education: education
    :type education: int
    :param power: power points
    :type power: int
    :param dexterity: dexterity points
    :type dexterity: int
    :param appearance: appearance points
    :type appearance: int
    :param strength: strength points
    :type strength: int
    :param occupation: occupation can accept any valid occupation defined in "occupations.json". Additionally, it can accept "optimal" or "random" option. "optimal" will return occupations that gives the highest amount of occupation points based on provided characteristics. "random" will return completely random occupation regardless provides characteristics, defaults to "optimal"
    :type occupation: str, optional
    :raises ValueError: raise if occupation in not in [optimal, random]
    :return: occupation
    :rtype: str
    """
    # TODO: check why there is None
    if occupation not in OCCUPATIONS_LIST + ["optimal", "random", None]:
        raise ValueError("occupation incorrect")

    # TODO: What happen if user provide illegal values, strings or below 0?
    skill_points_groups: tuple[int] = (
        education * 4,  # 1
        education * 2 + power * 2,  # 2
        education * 2 + dexterity * 2,  # 3
        education * 2 + appearance * 2,  # 4
        education * 2 + strength * 2,  # 5
    )

    if occupation == "random":
        occupation = random.choice(OCCUPATIONS_LIST)

    if occupation == "optimal":
        skill_points: int = max(skill_points_groups)
        candidates_for_occupation: List[str] = random.choice(
            [
                group
                for index, group in enumerate(OCCUPATIONS_GROUPS)
                if skill_points_groups[index] == skill_points
            ]
        )
        occupation = random.choice(candidates_for_occupation)

    return occupation


# TODO: write unit test
def get_occupation_points(
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
    :param occupation_points: occupation_points, defaults to None
    :type occupation_points: int, optional
    :return: occupation points for provided occupation
    :rtype: int
    """
    return (
        occupation_points
        if occupation_points
        else get_skill_points(
            occupation, education, power, dexterity, appearance, strength
        )
    )


# TODO: write unit test
def get_hobby_points(intelligence: int, hobby_points: int = None) -> int:
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
