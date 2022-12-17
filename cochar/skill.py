"""**Skills**
Skills module contains all functions related with skills
and Skills object, which is a container for skills

"""
import random
from collections import UserDict
from typing import Dict, List

import cochar
import cochar.error
import cochar.interface
import cochar.utils

Skill = Dict[str, int]

# TODO: write unit test
class SkillsDict(UserDict):
    """Dictionary like object to store character's skills.
    Override __setitem__ to validate skills data.

    :param UserDict: UserDict from collections
    :type UserDict: abc.ABCMeta
    """

    def get_json_format(self):
        """Return Skills as a dictionary"""
        return {k: v for k, v in self.items()}

    def __setitem__(self, key: str, value: int) -> None:
        """Add validation for skill values

        :param key: skill name
        :type key: str
        :param value: skill value
        :type value: int
        :raises SkillValueNotAnInt: when value is not an integer
        :raises SkillPointsBelowZero: when value is less than 0
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
        skills: SkillsDict = None,
    ) -> SkillsDict:
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
            skills = SkillsDict(skills)
        else:
            skills = SkillsDict()

            self.skills_data["doge"] = dexterity // 2
            self.skills_data["language (own)"] = education

            # Assigning points to credit rating
            credit_rating_points = generate_credit_rating_points(
                occupation, occupation_points
            )

            occupation_points_to_distribute = occupation_points - credit_rating_points

            if occupation_points_to_distribute < 0:
                occupation_points_to_distribute = 0

            default_occupations_skills: list = cochar.OCCUPATIONS_DATA[occupation][
                "skills"
            ].copy()
            occupation_skills_list = self._get_skills_list(default_occupations_skills)

            hobby_skills_list = self._get_skills_list(self.skills_basic)

            skills = self._assign_skill_points(
                occupation_points, occupation_skills_list, skills
            )
            skills = self._assign_skill_points(hobby_points, hobby_skills_list, skills)
            skills = self._filter_skills(skills)

            skills.setdefault("credit rating", credit_rating_points)

        return skills

    def _get_skills_list(self, input_list: list) -> List[str]:
        """Parse an input list taken from `occupations.json` and
        return list of skills

        :param input_list: list of skills from `occupations.json`
        :type input_list: list
        :return: list of skills
        :rtype: List[str]
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

    def _get_choice_skills(self, skills_list: list) -> List[str]:
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

    def _get_category_skills(self, skills_list: list) -> List[str]:
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
            if skill in self.skills_all:
                skills.setdefault(skill, self.skills_data[skill])
            else:
                skills.setdefault(skill, 1)

        while points:
            skill = random.choice(skills_list)
            if points <= cochar.MAX_SKILL_LEVEL - skills[skill]:
                points_allocation = random.randint(0, points)
            elif sum(list(skills.values())) % 90 == 0:
                break
            elif skills[skill] >= cochar.MAX_SKILL_LEVEL:
                continue
            else:
                points_allocation = random.randint(
                    0, cochar.MAX_SKILL_LEVEL - skills[skill]
                )
            skills[skill] += points_allocation
            points -= points_allocation

        return skills

    def _filter_skills(self, skills: Dict) -> SkillsDict:
        """Filter out all skills with basic value form given dict.

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

    :param occupation: occupation
    :type occupation: str
    :param occupation_points: occupation points
    :type occupation_points: int
    :return: credit rating points
    :rtype: int
    """
    credit_rating_range = cochar.OCCUPATIONS_DATA[occupation]["credit_rating"].copy()
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
        index
        for index, group in enumerate(cochar.OCCUPATIONS_GROUPS)
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
