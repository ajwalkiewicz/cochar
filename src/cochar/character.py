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
""" "This module contains classes related with Character object itself."""

from abc import ABC, abstractmethod
from typing import Any, override

import randname

import cochar.config
import cochar.error
import cochar.skill


class Validator(ABC):
    """It's a parent class for all other descriptors.

    Defines validate method, that needs to be implemented by
    all children.
    """

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value) -> None:
        pass


class Characteristic(Validator):
    """Base characteristic for character class"""

    def __init__(self, min_value: int) -> None:
        self.min_value = min_value

    @override
    def validate(self, value: int) -> None:
        """Check if characteristic is a valid number and is not below `min_value`

        Args:
            value: value to validate


        Raises:
            cochar.error.CharacteristicValueNotAnInt: raise if value is not an integer
            cochar.error.CharacteristicPointsBelowMinValue: raise if value is below min_value
        """
        if not isinstance(value, int):
            raise cochar.error.CharacteristicValueNotAnInt(self.public_name, value)
        if value < self.min_value:
            raise cochar.error.CharacteristicPointsBelowMinValue(value, self.min_value)


class Name(Validator):
    """Character's name"""

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, str(value))

    @override
    def validate(self, value: str) -> None:
        """Check if name is a valid name.

        Args:
            value: new character name

        Raises:
            cochar.error.EmptyName: raise if `value` is empty
        """
        if value == "":
            raise cochar.error.EmptyName()
        self._first_name = str(value)


class Year(Validator):
    """Year in game.

    Technically any integer is a valid year. But practically that depends
    on database with names used to generate names.

    Besides name, also character's age depends on the year. Probability of
    generating certain year is related with the population age pyramid at the
    certain year.

    Lowest and highest year in the data defines effective range for year. Years
    below or above are treated the same as in the lowest or highest years in data.
    That means for example if data for names ends on the year 2010, than setting
    higher year will give same results as 2010.
    """

    @override
    def validate(self, value: int) -> None:
        """Validate if year is an integer.

        Args:
            value: new year of the game

        Raises:
            cochar.error.InvalidYearValue: raise when `value` is not an integer

        Examples:
            >>> character = create_character()
            >>> character.year = 1800
        """
        if not isinstance(value, int):
            raise cochar.error.InvalidYearValue(value)


class Sex(Validator):
    """Character's sex.

    Available sex options:
    - M: male
    - F: female
    - None: for non binary

    As there are not any data for non binary names.
    When ``None`` is selected sex will be randomly drawn from M or F

    Examples:
        >>> c = Character(year=1925, country="US", sex="F")
        >>> c.sex
        'F'
    """

    @override
    def validate(self, value: str | None) -> None:
        """
        Validate character's sex.

        Args:
            value: character's new sex

        Raises:
            cochar.error.InvalidSexValue: Incorrect sex value: sex -> ['M', 'F', None]
        """
        if value not in cochar.config.SEX_OPTIONS:
            raise cochar.error.InvalidSexValue(value, cochar.config.SEX_OPTIONS)


class Age(Validator):
    """Character's age.

    Warning:
        Age must be between `min_age` and `max_age` defined during
        descriptor initialization.
    """

    def __init__(self, min_age: int, max_age: int) -> None:
        """Initialize age descriptor.

        Args:
            min_age: minimal character's age
            max_age: maximal character's age
        """
        self.min_age = min_age
        self.max_age = max_age

    @override
    def validate(self, value: int) -> None:
        """
        Validate character's age.

        Args:
            value: character's new age

        Raises:
            cochar.error.InvalidAgeValue: raise when age is not an integer
            cochar.error.AgeNotInRange: age must be between min and max age
        """
        if not isinstance(value, int):
            raise cochar.error.InvalidAgeValue(value)

        if not self.min_age <= value <= self.max_age:
            raise cochar.error.AgeNotInRange(value, self.min_age, self.max_age)


class Country(Validator):
    """Character's country.

    Country depends on available data. By default database from
    external `randname` package is taken.
    Country also defines what dataset will be used for generating character's
    name.

    See `randname.available_countries()`.
    """

    @override
    def validate(self, value: str) -> None:
        """
        Validate character's country.

        Args:
            value: character's new country

        Raises:
            cochar.error.InvalidCountryValue: "Country not available: {value} -> {randname.available_countries()}
        """

        available_countries = randname.available_countries()
        if value not in available_countries:
            raise cochar.error.InvalidCountryValue(value, available_countries)


class Occupation(Validator):
    """Character's occupation.

    Available occupations are defined in occupation database.
    """

    def __init__(self, available_occupations):
        self.available_occupations = available_occupations

    @override
    def validate(self, value: str) -> None:
        """
        Validate character's occupation.

        Args:
            value: character's new occupation

        Raises:
            cochar.error.InvalidOccupationValue: raise when `value` is not in `OCCUPATION_LIST`
        """
        if value not in self.available_occupations:
            raise cochar.error.InvalidOccupationValue(value, self.available_occupations)


class DamageBonus(Validator):
    """Character damage bonus.

    ``correct_values = ['-2', '-1', '0', '+1K4', '+1K6', '+2K6', '+3K6', '+4K6', '+5K6']``

    """

    @override
    def validate(self, value: str) -> None:
        """
        Validate character's damage bonus.

        Args:
            value: character's new damage bonus

        Raises:
            cochar.error.InvalidDamageBonusValue: Invalid damage bonus. {value} not in {correct_values}
        """
        # TODO: Increase range. +1 for each 80 point above STR+SIZ
        correct_values = [
            "-2",
            "-1",
            "0",
            "+1K4",
            "+1K6",
            "+2K6",
            "+3K6",
            "+4K6",
            "+5K6",
        ]
        new_damage_bonus = str(value).upper()
        if new_damage_bonus not in correct_values:
            raise cochar.error.InvalidDamageBonusValue(new_damage_bonus, correct_values)


class Build(Validator):
    """Character's build.

    Warning:
        `correct_values = [-2, -1, 0, 1, 2, 3, 4, 5, 6]`

    TODO: increase range. +1 for each 80 point above STR+SIZ.
    """

    @override
    def validate(self, value: int) -> None:
        """
        Validate character's build.

        Args:
            value: character's new build

        Raises:
            cochar.error.InvalidBuildValue: Invalid build. {value} not in {correct_values}
        """
        correct_values = [-2, -1, 0, 1, 2, 3, 4, 5, 6]
        if value not in correct_values:
            raise cochar.error.InvalidBuildValue(value, correct_values)


class Character:
    """Container for character.

    Warning:
        Although this class can be used as standalone class,
        it is advised to use `cochar.create_character()` function
        to generate character.
    """

    # Characteristics descriptors
    strength = Characteristic(min_value=0)
    condition = Characteristic(min_value=0)
    size = Characteristic(min_value=0)
    dexterity = Characteristic(min_value=0)
    appearance = Characteristic(min_value=0)
    education = Characteristic(min_value=0)
    intelligence = Characteristic(min_value=0)
    power = Characteristic(min_value=0)
    luck = Characteristic(min_value=0)
    power = Characteristic(min_value=0)
    move_rate = Characteristic(min_value=0)
    sanity_points = Characteristic(min_value=0)
    magic_points = Characteristic(min_value=0)
    hit_points = Characteristic(min_value=0)
    dodge = Characteristic(min_value=0)

    # Name descriptors
    first_name = Name()
    last_name = Name()

    # Other descriptors
    year = Year()
    sex = Sex()
    age = Age(min_age=cochar.config.MIN_AGE, max_age=cochar.config.MAX_AGE)
    country = Country()
    occupation = Occupation(available_occupations=cochar.config.OCCUPATIONS_LIST)
    damage_bonus = DamageBonus()
    build = Build()

    def __init__(
        self,
        year: int = 0,
        country: str = "",
        first_name: str = "",
        last_name: str = "",
        age: int = 0,
        sex: str = "",
        occupation: str = "",
        strength: int = 0,
        condition: int = 0,
        size: int = 0,
        dexterity: int = 0,
        appearance: int = 0,
        education: int = 0,
        intelligence: int = 0,
        power: int = 0,
        luck: int = 0,
        move_rate: int = 0,
        damage_bonus: str = "0",
        build: int = 0,
        dodge: int = 0,
        skills: cochar.skill.SkillsDict | None = None,
        sanity_points: int = 0,
        magic_points: int = 0,
        hit_points: int = 0,
    ) -> None:
        self.year = year
        self.country = country
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.occupation = occupation
        self.strength = strength
        self.condition = condition
        self.size = size
        self.dexterity = dexterity
        self.appearance = appearance
        self.education = education
        self.intelligence = intelligence
        self.power = power
        self.move_rate = move_rate
        self.luck = luck
        self.damage_bonus = damage_bonus
        self.build = build

        if skills is None:
            self.skills = cochar.skill.SkillsDict()
        else:
            self.skills = skills

        self.dodge = dodge
        self.sanity_points = sanity_points
        self.magic_points = magic_points
        self.hit_points = hit_points

    @property
    def skills(self) -> cochar.skill.SkillsDict:
        """Character's skills.

        Returns:
            character's skills
        """
        return self._skills

    @skills.setter
    def skills(self, new_skills: dict | cochar.skill.SkillsDict) -> None:
        if isinstance(new_skills, cochar.skill.SkillsDict):
            self._skills = new_skills
        elif isinstance(new_skills, dict):
            self._skills = cochar.skill.SkillsDict(new_skills)
        else:
            raise cochar.error.SkillsNotADict("Invalid skills. Skills must be a dict")

    def get_json_format(self) -> dict[str, Any]:
        """Return character's full characteristics as a dictionary.

        :return: full characteristics
        """
        result = {str(key)[1:]: value for key, value in vars(self).items()}
        result.update({"skills": self.skills.get_json_format()})
        return result

    def __eq__(self, o: object) -> bool:
        return True if self.__dict__ == o.__dict__ else False

    def __repr__(self) -> str:
        return (
            f"Character(year={self.year}, country='{self.country}', "
            f"first_name='{self.first_name}', last_name='{self.last_name}', "
            f"age={self.age}, sex='{self.sex}', occupation='{self.occupation}', "
            f"strength={self.strength}, condition={self.condition}, size={self.size}, "
            f"dexterity={self.dexterity}, appearance={self.appearance}, education={self.education}, "
            f"intelligence={self.intelligence}, power={self.power}, move_rate={self.move_rate}, "
            f"luck={self.luck}, skills={self.skills}, damage_bonus='{self.damage_bonus}', "
            f"build={self.build}, dodge={self.dodge}, sanity_points={self.sanity_points}, "
            f"magic_points={self.magic_points}, hit_points={self.hit_points})"
        )

    def __str__(self) -> str:
        skills = ""
        max_items_in_row = 3
        current_number_of_items_in_row = 0

        for skill, value in self._skills.items():
            if current_number_of_items_in_row == max_items_in_row:
                skills += "\n"
                current_number_of_items_in_row = 0
            skills += f"| {skill.capitalize()}: {value} |"
            current_number_of_items_in_row += 1

        return (
            f"Character\n"
            f"Name: {self.first_name} {self.last_name}\n"
            f"Sex: {self.sex}, Age: {self.age}, Country: {self.country}\n"
            f"Occupation: {self.occupation.capitalize()}\n"
            f"STR: {self.strength} CON: {self.condition} SIZ: {self.size}\n"
            f"DEX: {self.dexterity} APP: {self.appearance} EDU: {self.education}\n"
            f"INT: {self.intelligence} POW: {self.power} Luck: {self.luck}\n"
            f"Damage bonus: {self.damage_bonus}\n"
            f"Build: {self.build}\n"
            f"Dodge: {self.dodge}\n"
            f"Move rate: {self.move_rate}\n"
            f"Skills:\n"
            f"{skills}"
        )
