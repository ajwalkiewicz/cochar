# Cochar - create a random character for Call of Cthulhu RPG 7th ed.
# Copyright (C) 2023  Adam Walkiewicz

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""**Occupations**
Occupations is a module that contains functions related
with occupations
"""

import copy
import random
from itertools import compress
from typing import List

import cochar
import cochar.config
import cochar.error
import cochar.skill


def generate_occupation(
    education: int = 1,
    power: int = 1,
    dexterity: int = 1,
    appearance: int = 1,
    strength: int = 1,
    random_mode: bool = False,
    occupation: str | None = None,
    occup_type: str | None = None,
    era: list[str] | None = None,
    tags: list[str] | None = None,
) -> str:
    """Return occupation based on:
    education, power, dexterity, appearance and strength.

    Args:
        education: education points, defaults to 1
        power: power points, defaults to 1
        dexterity: dexterity points, defaults to 1
        appearance: appearance points, defaults to 1
        strength: strength points, defaults to 1
        random_mode: ignore edu, pow, dex and str points and return totally random occupation, defaults to False
        occupation: return specified occupation, defaults to None
        occup_type: specify type of occupation to return, defaults to None
        era: specify era of occupation to return, defaults to None
        tags: return occupation with defined tags, defaults to None

    Raises:
        cochar.error.IncorrectOccupation: when occupation is not in the list of available occupations
        cochar.error.NoneOccupationMeetsCriteria: when searching criteria are not met by any occupation

    Returns:
        occupation name
    """
    # TODO: What happen if user provide illegal values, strings or below 0?
    skill_points_groups: list[int] = [
        education * 4,  # 1
        education * 2 + power * 2,  # 2
        education * 2 + dexterity * 2,  # 3
        education * 2 + appearance * 2,  # 4
        education * 2 + strength * 2,  # 5
    ]

    if random_mode:
        return random.choice(cochar.config.OCCUPATIONS_LIST)

    if occupation:
        if occupation not in cochar.config.OCCUPATIONS_LIST:
            raise cochar.error.IncorrectOccupation(occupation)
        return occupation

    occupation_groups = copy.deepcopy(cochar.config.OCCUPATIONS_GROUPS)

    if occup_type:
        for i, group in enumerate(occupation_groups):
            occupation_groups[i] = [
                occup
                for occup in group
                if cochar.config.OCCUPATIONS_DATA[occup]["type"] == occup_type
            ]

    if era:
        for i, group in enumerate(occupation_groups):
            occupation_groups[i] = [
                occup
                for occup in group
                if cochar.config.OCCUPATIONS_DATA[occup]["era"] in era
            ]

    if tags:
        for i, group in enumerate(occupation_groups):
            occupation_groups[i] = [
                occup
                for occup in group
                if set(tags).issubset(
                    set(cochar.config.OCCUPATIONS_DATA[occup]["tags"])
                )
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
    occupation_points: int | None = None,
) -> int:
    """Return occupation points based on occupation, education, power,
    dexterity, appearance and strength.

    If `occupation_points` provided, return `occupation_points`

    Args:
        occupation: occupation points
        education: education points
        power: power points
        dexterity: dexterity points
        appearance: appearance points
        strength: strength points
        occupation_points: occupation points, if provided function returns that value instead of calculating it, defaults to None

    Returns:
        occupation points for provided occupation
    """
    return (
        occupation_points
        if occupation_points is not None
        else cochar.skill.calc_skill_points(
            occupation, education, power, dexterity, appearance, strength
        )
    )


def calc_hobby_points(intelligence: int, hobby_points: int | None = None) -> int:
    """Return hobby points, based on intelligence.

    occupation points = 2 * intelligence

    If `hobby_points` provided, return `hobby_points`

    Args:
        intelligence: intelligence points
        hobby_points: hobby_points, defaults to None

    Returns:
        hobby points
    """
    return hobby_points if hobby_points else intelligence * 2


def get_occupation_list():
    return sorted(cochar.config.OCCUPATIONS_LIST)
