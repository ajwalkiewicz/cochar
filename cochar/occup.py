"""**Occupations**
Occupations is a module that contains functions related
with occupations
"""
import random
from typing import List, Tuple

import cochar
import cochar.skill


# TODO: write unit test
def get_occupation(
    education: int,
    power: int,
    dexterity: int,
    appearance: int,
    strength: int,
    random_mode: bool = False,
    occupation: str = None,
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
    :param random_mode: choose occupation completely randomly, regardless the character's statistics, defaults to "False"
    :type random_mode: bool, optional
    :param occupation: character's occupation return provided occupation as character's occupation if it exists, defaults to "None"
    :type occupation: str, optional
    :raises ValueError: raise if occupation in not in [optimal, random]
    :return: occupation
    :rtype: str
    """
    # TODO: What happen if user provide illegal values, strings or below 0?
    skill_points_groups: tuple[int] = (
        education * 4,  # 1
        education * 2 + power * 2,  # 2
        education * 2 + dexterity * 2,  # 3
        education * 2 + appearance * 2,  # 4
        education * 2 + strength * 2,  # 5
    )

    if random_mode:
        return random.choice(cochar.OCCUPATIONS_LIST)

    if occupation:
        if occupation not in cochar.OCCUPATIONS_LIST:
            raise ValueError(f"Incorrect occupation: {occupation}")
        return occupation

    skill_points: int = max(skill_points_groups)
    candidates_for_occupation: List[str] = random.choice(
        [
            group
            for index, group in enumerate(cochar.OCCUPATIONS_GROUPS)
            if skill_points_groups[index] == skill_points
        ]
    )
    return random.choice(candidates_for_occupation)


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
        else cochar.skill.get_skill_points(
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
