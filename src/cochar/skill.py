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
"""**Skills**
Skills module contains all functions related with skills
and Skills object, which is a container for skills

"""

import random
from collections import UserDict

import cochar
import cochar.config
import cochar.error
import cochar.interface
import cochar.utils

Skill = dict[str, int]


# TODO: write unit test
class SkillsDict(UserDict):
    """Dictionary like object to store character's skills.
    Override __setitem__ to validate skills data.
    """

    def get_json_format(self):
        """Return Skills as a dictionary"""
        return {k: v for k, v in self.items()}

    def __setitem__(self, key: str, value: int) -> None:
        """Add validation for skill values

        Args:
            key: skill name
            value: skill value

        Raises:
            cochar.error.SkillValueNotAnInt: when value is not an integer
            cochar.error.SkillPointsBelowZero: when value is less than 0
        """
        key = str(key)
        if not isinstance(value, int):
            raise cochar.error.SkillValueNotAnInt(
                f"Invalid {key.lower()} points. {key.capitalize()} points must be an integer"
            )
        if value < 0:
            raise cochar.error.SkillPointsBelowZero(
                f"{key.capitalize()} points cannot be less than 0"
            )
        self.data[key] = value


class SkillsGenerator:
    def __init__(self, interface: cochar.interface.SkillsDataInterface):
        self.set_interface(interface)

    def set_interface(self, interface: cochar.interface.SkillsDataInterface) -> None:
        self.interface = interface
        self.skills_data = self.interface.get_skills()
        self.skills_all = self.interface.get_all_skills_names()
        self.skills_basic = self.interface.get_basic_skills_names()
        self.skills_categories = self.interface.get_categories_names()

    def generate_skills(
        self,
        occupation: str,
        occupation_points: int,
        hobby_points: int,
        dexterity: int,
        education: int,
        skills: SkillsDict | None = None,
    ) -> SkillsDict:
        """Return skills based on:
        occupation, occupation_points, hobby_points, dexterity and education

        If `skills` provided, return `skills`

        Each occupation has related skills, that are chosen randomly. Then
        each skill has randomly assigned skill level - number of points related
        with that skill.

        Dexterity is required for `dodge` skill.
        Education is required for `language(own)` skill.

        Args:
            occupation: occupation
            occupation_points: occupation_points
            hobby_points: hobby_points
            dexterity: dexterity
            education: education
            skills: skills, defaults to None

        Returns:
            skills with assigned skill level
        """
        if skills:
            skills = SkillsDict(skills)
        else:
            skills = SkillsDict()

            self.skills_data["dodge"] = dexterity // 2
            self.skills_data["language (own)"] = education

            # Assigning points to credit rating
            credit_rating_points = generate_credit_rating_points(
                occupation, occupation_points
            )

            occupation_points_to_distribute = occupation_points - credit_rating_points

            if occupation_points_to_distribute < 0:
                occupation_points_to_distribute = 0

            default_occupations_skills: list = cochar.config.OCCUPATIONS_DATA[
                occupation
            ]["skills"].copy()
            occupation_skills_list = self._get_skills_list(default_occupations_skills)

            hobby_skills_list = self._get_skills_list(self.skills_basic)

            skills = self._assign_skill_points(
                occupation_points, occupation_skills_list, skills
            )
            skills = self._assign_skill_points(hobby_points, hobby_skills_list, skills)
            skills = self._filter_skills(skills)

            skills.setdefault("credit rating", credit_rating_points)

        return skills

    def _get_skills_list(self, input_list: list) -> list[str]:
        """Parse an input list taken from `occupations.json` and
                return list of skills

        Args:
            input_list: list of skills from `occupations.json`

        Returns:
            list of skills
        """
        skills_list = []
        skills_list += list(
            filter(
                lambda x: len(x) > 2
                and isinstance(x, str)
                and x not in self.skills_categories,
                input_list,
            )
        )
        skills_list += self._get_choice_skills(input_list)
        skills_list += self._get_category_skills(input_list)
        return skills_list

    def _get_choice_skills(self, skills_list: list) -> list[str]:
        """Parse a choice option from skills in `occupation.json` and
        return list of skills

        Example:
        [1, "occult", "natural world"] -> ["occult"]
        It means, return randomly one skills from the following options

        Args:
            skills_list: list of skills to choose

        Returns:
            list of skills
        """
        result = []
        for item in skills_list:
            if isinstance(item, list):
                population = item[1:]
                k = item[0]
                result.extend(random.sample(population, k=k))
                result.extend(self._get_category_skills(result))
                result = list(
                    filter(
                        lambda x: x not in self.interface.get_categories_names()
                        and len(x) > 2,
                        result,
                    )
                )

        return result

    def _get_category_skills(self, skills_list: list) -> list[str]:
        """Parse a category skills, and return list of skills.

        Example:
        "1l" -> ["language (german)"]
        It means, one random language from language group.
        "2*" -> ["first aid", "listen"]
        It means, two random skills of all available skills.

        Args:
            skills_list: list of category skill options

        Returns:
            list of skills
        """
        result = []
        for item in skills_list:
            if len(item) == 2 and isinstance(item, str):
                k = int(item[0])
                if item[1] == "*":
                    population = self.skills_basic
                else:
                    population = self.interface.get_skills_from_category(
                        cochar.utils.TRANSLATION_DICT.get(item[1])
                    )
                result.extend(random.sample(population, k=k))

            elif item in self.skills_categories:
                population = self.interface.get_skills_from_category(item)
                result.extend([random.choice(population)])

        return result

    def _assign_skill_points(
        self, points: int, skills_list: list, skills: SkillsDict
    ) -> SkillsDict:
        """Allocate randomly points to the skills from skills_list
        and store it in Skills object

        Args:
            points: points to allocate
            skills_list: list of skills
            skills: Skills object

        Returns:
            Skills object with allocated points
        """
        for skill in skills_list:
            if skill in self.skills_all:
                skills.setdefault(skill, self.skills_data[skill])
            else:
                skills.setdefault(skill, 1)

        while points:
            skill = random.choice(skills_list)
            if points <= cochar.config.MAX_SKILL_LEVEL - skills[skill]:
                points_allocation = random.randint(0, points)
            elif sum(list(skills.values())) % 90 == 0:
                break
            elif skills[skill] >= cochar.config.MAX_SKILL_LEVEL:
                continue
            else:
                points_allocation = random.randint(
                    0, cochar.config.MAX_SKILL_LEVEL - skills[skill]
                )
            skills[skill] += points_allocation
            points -= points_allocation

        return skills

    def _filter_skills(self, skills: dict[str, int]) -> SkillsDict:
        """Filter out all skills with basic value form given dict.

        Examples:
            >>> example_dict = {'psychoanalysis': 1, 'language (spanish)': 66}
            >>> SkillsGenerator(skills_interface)._filter_skills(example_dict)
            {'language (spanish)': 66}
        """

        def has_skill_default_value(item) -> bool:
            skill, value = item
            default_value = self.skills_data.get(skill)
            if default_value is not None:
                return default_value != value

            return False

        skills = filter(has_skill_default_value, skills.items())

        return SkillsDict(skills)


def generate_credit_rating_points(occupation: str, occupation_points: int) -> int:
    """For provided occupation, and it occupation points, return
    credit rating points.

    Args:
        occupation: occupation
        occupation_points: occupation points

    Returns:
        credit rating points
    """
    credit_rating_range = cochar.config.OCCUPATIONS_DATA[occupation][
        "credit_rating"
    ].copy()
    if occupation_points < min(credit_rating_range):
        credit_rating_range = [0, occupation_points]
    if occupation_points < max(credit_rating_range):
        credit_rating_range[1] = occupation_points
    return random.randint(*credit_rating_range)


def calc_skill_points(
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

    Args:
        occupation: occupation name
        education: education points
        power: power points
        dexterity: dexterity points
        appearance: appearance points
        strength: strength points

    Returns:
        skill points
    """
    skill_points_groups: tuple[int, ...] = (
        education * 4,  # 1
        education * 2 + power * 2,  # 2
        education * 2 + dexterity * 2,  # 3
        education * 2 + appearance * 2,  # 4
        education * 2 + strength * 2,  # 5
    )
    group_index = [
        index
        for index, group in enumerate(cochar.config.OCCUPATIONS_GROUPS)
        if occupation in group
    ]
    points = [skill_points_groups[i] for i in group_index]

    return max(points)


def skill_test(tested_value: int, repetition: int = 1) -> int:
    """Perform skill test.

    Works like improvement test. Roll number between 1 to 100,
    If that number is higher than tested value or higher,
    than 95, then increase tested value with random number,
    between 1 to 10.

    Repeat repetition times.

    Notes::
        for characteristics use `characteristic_test()`

    Args:
        tested_value: tested value
        repetition: how many test to perform

    Returns:
        unchanged, or increased tested value
    """
    for _ in range(repetition):
        test = random.randint(1, 100)
        if test > tested_value or test > 95:
            tested_value += random.randint(1, 10)
    return tested_value
