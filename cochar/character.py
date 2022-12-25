""""This module contains classes related with Character object itself."""

from abc import ABC, abstractmethod
from typing import List, Union

import randname

import cochar
import cochar.cochar
import cochar.error
import cochar.skill


class Validator(ABC):
    """It's a parent class for all other descriptors.

    Defines validate method, that needs to be implemented by
    all children.

    :param ABC: abstract base class
    :type ABC: ABCMeta
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
    def validate(self, value):
        pass


class Characteristic(Validator):
    """Base characteristic for character class"""

    def __init__(self, min_value=None):
        self.min_value = min_value

    def validate(self, value: int):
        """Check if characteristic is a valid number and is not below `min_value`

        :param value: value to validate
        :type value: int
        :raises cochar.error.CharacteristicValueNotAnInt: raise if value is not an integer
        :raises cochar.error.CharacteristicPointsBelowZero: raise if value is below min_value
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

    def validate(self, new_name: str):
        """Check if name is a valid name.

        :param new_name: new character name
        :type new_name: str
        :raises cochar.error.EmptyName: raise if `new_name` is empty
        """
        if new_name == "":
            raise cochar.error.EmptyName()
        self._first_name = str(new_name)


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

    def validate(self, new_year: int) -> None:
        """Validate if year is an integer.

        :param new_year: new year of the game
        :type new_year: int
        :raises cochar.error.InvalidYearValue: raise when `new_year` is not an integer

        >>> character = create_character()
        >>> character.year = 1800
        """
        if not isinstance(new_year, int):
            raise cochar.error.InvalidYearValue(new_year)


class Sex(Validator):
    """Character's sex.

    Available sex options:
    - M: male
    - F: female
    - None: for non binary

    As there are not any data for non binary names.
    When ``None`` is selected sex will be randomly drawn from M or F

    >>> c = Character(year=1925, country="US", sex="F")
    >>> c.sex
    'F'
    """

    def validate(self, new_sex: Union[str, None]) -> None:
        """
        Validate character's sex.

        :param new_sex: character's new sex
        :type new_sex: str | None
        :raises InvalidSexValue: Incorrect sex value: sex -> ['M', 'F', None']
        """
        if new_sex not in cochar.SEX_OPTIONS:
            raise cochar.error.InvalidSexValue(new_sex, cochar.SEX_OPTIONS)


class Age(Validator):
    """Character's age.

    :param min_age: minimal character's age
    :type min_age: int
    :param max_age: maximal character's age
    :type max_age: int
    """

    def __init__(self, min_age: int, max_age: int) -> None:
        self.min_age = min_age
        self.max_age = max_age

    def validate(self, new_age: int) -> None:
        """
        Validate character's age.

        :param new_age: character's new age
        :type new_age: int
        :raises InvalidAgeValue: raise when age is not an integer
        :raises AgeNotInRange: age must be between min and max age
        """
        if not isinstance(new_age, int):
            raise cochar.error.InvalidAgeValue(new_age)

        if not self.min_age <= new_age <= self.max_age:
            raise cochar.error.AgeNotInRange(new_age, self.min_age, self.max_age)


class Country(Validator):
    """Character's country.

    Country depends on available data. By default database from
    external ``randname`` package is taken.
    Country also defines what dataset will be used for generating character's
    name.

    See ``randname.available_countries()``.
    """

    def validate(self, new_country: str) -> None:
        """
        Validate character's country.

        :param new_country: character's new country
        :type new_country: str
        :raises InvalidCountryValue: "Country not available: {new_country} -> {randname.available_countries()}
        """

        available_countries = randname.available_countries()
        if new_country not in available_countries:
            raise cochar.error.InvalidCountryValue(new_country, available_countries)


class Occupation(Validator):
    """Character's occupation.

    Available occupations are defined in occupation database.
    """

    def __init__(self, available_occupations):
        self.available_occupations = available_occupations

    def validate(self, new_occupation: str) -> None:
        """
        Validate character's occupation.

        :param new_occupation: character's new occupation
        :type new_occupation: str
        :raises InvalidOccupationValue: raise when `new_occupation` is not in `OCCUPATION_LIST`
        """
        if new_occupation not in self.available_occupations:
            raise cochar.error.InvalidOccupationValue(
                new_occupation, self.available_occupations
            )


class DamageBonus(Validator):
    """Character damage bonus.

    ``correct_values = ['-2', '-1', '0', '+1K4', '+1K6', '+2K6', '+3K6', '+4K6', '+5K6']``

    """

    def validate(self, new_damage_bonus: str) -> None:
        """
        Validate character's damage bonus.

        :param new_damage_bonus: character's new damage bonus
        :type new_damage_bonus: str
        :raises InvalidDamageBonusValue: Invalid damage bonus. {new_damage_bonus} not in {correct_values}
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
        new_damage_bonus = str(new_damage_bonus).upper()
        if new_damage_bonus not in correct_values:
            raise cochar.error.InvalidDamageBonusValue(new_damage_bonus, correct_values)


class Build(Validator):
    """Character's build.

    ``correct_values = [-2, -1, 0, 1, 2, 3, 4, 5, 6]``

    TODO: increase range. +1 for each 80 point above STR+SIZ.
    """

    def validate(self, new_build: int) -> None:
        """
        Validate character's build.

        :param new_build: character's new build
        :type new_build: int
        :raises InvalidBuildValue: Invalid build. {new_build} not in {correct_values}
        """
        correct_values = [-2, -1, 0, 1, 2, 3, 4, 5, 6]
        if new_build not in correct_values:
            raise cochar.error.InvalidBuildValue(new_build, correct_values)


class Character:
    """Container for character.

    .. warning:
        Although this class can be used as standalone class,
        it is advised to use `cochar.create_character()` function
        to generate character.
    """

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
    doge = Characteristic(min_value=0)

    first_name = Name()
    last_name = Name()

    year = Year()
    sex = Sex()
    age = Age(min_age=cochar.MIN_AGE, max_age=cochar.MAX_AGE)
    country = Country()
    occupation = Occupation(available_occupations=cochar.OCCUPATIONS_LIST)
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
        damage_bonus: str = 0,
        build: int = 0,
        doge: int = 0,
        skills: cochar.skill.SkillsDict = {},
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
        self.skills = cochar.skill.SkillsDict(skills)
        self.doge = doge
        self.sanity_points = sanity_points
        self.magic_points = magic_points
        self.hit_points = hit_points

    @property
    def skills(self) -> cochar.skill.SkillsDict:
        """Character's skills.

        :return: character's skills
        :rtype: cochar.skill.Skills
        """
        return self._skills

    @skills.setter
    def skills(self, new_skills: Union[dict, cochar.skill.SkillsDict]) -> None:
        if isinstance(new_skills, cochar.skill.SkillsDict):
            self._skills = new_skills
        elif isinstance(new_skills, dict):
            self._skills = cochar.skill.SkillsDict(new_skills)
        else:
            raise cochar.error.SkillsNotADict("Invalid skills. Skills must be a dict")

    def get_json_format(self) -> dict:
        """Return character's full characteristics as a dictionary.

        :return: full characteristics
        :rtype: dict
        """
        result = {str(key)[1:]: value for key, value in vars(self).items()}
        result.update({"skills": self.skills.get_json_format()})
        return result

    def __eq__(self, o: object) -> bool:
        return True if self.__dict__ == o.__dict__ else False

    def __repr__(self) -> str:
        return (
            f"Character(year={self._year}, country='{self._country}', "
            f"first_name='{self._first_name}', last_name='{self._last_name}', "
            f"age={self._age}, sex='{self._sex}', occupation='{self._occupation}', "
            f"strength={self._strength}, condition={self._condition}, size={self._size}, "
            f"dexterity={self._dexterity}, appearance={self._appearance}, education={self._education}, "
            f"intelligence={self._intelligence}, power={self._power}, move_rate={self._move_rate}, "
            f"luck={self._luck}, skills={self._skills}, damage_bonus='{self._damage_bonus}', "
            f"build={self._build}, doge={self._doge}, sanity_points={self._sanity_points}, "
            f"magic_points={self._magic_points}, hit_points={self._hit_points})"
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
            f"Name: {self._first_name} {self._last_name}\n"
            f"Sex: {self._sex}, Age: {self._age}, Country: {self._country}\n"
            f"Occupation: {self._occupation.capitalize()}\n"
            f"STR: {self._strength} CON: {self._condition} SIZ: {self._size}\n"
            f"DEX: {self._dexterity} APP: {self._appearance} EDU: {self._education}\n"
            f"INT: {self._intelligence} POW: {self._power} Luck: {self._luck}\n"
            f"Damage bonus: {self._damage_bonus}\n"
            f"Build: {self._build}\n"
            f"Doge: {self._doge}\n"
            f"Move rate: {self._move_rate}\n"
            f"Skills:\n"
            f"{skills}"
        )
