import random
import os
import json
from typing import List, Tuple

from .skills import get_skill_points
from .settings import OCCUPATIONS_LIST, OCCUPATIONS_GROUPS


def get_occupation(
    education, power, dexterity, appearance, strength, occupation: str = "optimal"
) -> str:
    """[summary]

    :param occupation: [description], defaults to "optimal"
    :type occupation: str, optional
    :return: [description]
    :rtype: str
    """
    if occupation not in OCCUPATIONS_LIST + ["optimal", "random", None]:
        raise ValueError("occupation incorrect")

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


def get_occupation_points(
    occupation: str,
    education: int,
    power: int,
    dexterity: int,
    appearance: int,
    strength: int,
    occupation_points: int = None,
):
    return (
        occupation_points
        if occupation_points
        else get_skill_points(
            occupation, education, power, dexterity, appearance, strength
        )
    )


def get_hobby_points(intelligence, hobby_points: int = None) -> int:
    return hobby_points if hobby_points else intelligence * 2
