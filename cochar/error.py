"""
**Errors for cochar module**
"""
from typing import Any


class CocharError(Exception):
    pass


class IncorrectOccupation(CocharError):
    """Raise when occupation is not in OCCUPATIONS_LIST"""

    def __init__(self, occupation_name: str):
        self.occupation_name = occupation_name
        self.message = f"'{self.occupation_name.capitalize()}' not in available occupations. Check cochar.OCCUPATIONS_LIST"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class CharacteristicValueNotAnInt(CocharError):
    """Characteristic value has to be an integer number"""

    def __init__(self, skill_name: str, skill_value: Any):
        self.skill_name = skill_name
        self.skill_value = skill_value
        self.message = f"{self.skill_name.capitalize()} points must be an integer: '{self.skill_value}'"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class CharacteristicPointsBelowMinValue(CocharError):
    """Characteristic points cannot be below defined minimal value"""

    def __init__(self, skill_name: str, min_value=0):
        self.skill_name = skill_name
        self.min_value = min_value
        self.message = f"'{self.skill_name}' Characteristic points cannot be below: {self.min_value}"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class SkillValueNotAnInt(CocharError):
    """Skill value has to be an integer number"""

    def __init__(self, skill):
        self.skill = skill
        self.message = f"'{self.skill}' Skill value must be an integer"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class SkillPointsBelowZero(CocharError):
    """Skill points cannot be below zero"""

    def __init__(self, skill):
        self.skill = skill
        self.message = f"'{self.skill}' Skill points cannot be below zero"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class SkillsNotADict(CocharError):
    """Skills must be a dictionary"""

    def __init__(self, skill):
        self.skill = skill
        self.message = f"Invalid skills: '{self.skill}'. Skills must be an dictionary"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidYearValue(CocharError):
    """Year must be an integer number"""

    def __init__(self, year: int):
        self.year = year
        self.message = f"Invalid year: '{self.year}'. Year must be an integer number"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidSexValue(CocharError):
    """InvalidSexArgument.

    Raise when selected sex is not it available for chosen country.
    """

    def __init__(self, sex: str, available_sex: list):
        self.sex = sex
        self.available_sex = available_sex
        self.message = f"{self.sex} not in {self.available_sex}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.sex} -> {self.message}."


class EmptyName(CocharError):
    """Name cannot be an empty string"""

    def __str__(self):
        return "Name cannot be an empty string"


class AgeNotInRange(CocharError):
    """Age must be within specified range, default 15 - 90"""

    def __init__(self, age: int, min_age: int, max_age: int):
        self.age = age
        self.min_age = min_age
        self.max_age = max_age
        self.message = (
            f"Age not in range: {self.age} -> [{self.min_age}, {self.max_age}]"
        )
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}."


class InvalidAgeValue(CocharError):
    """Age must be an integer number"""

    def __init__(self, age: int):
        self.age = age
        self.message = f"'{self.age}' Age must be an integer number"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidCountryValue(CocharError):
    """Raise when country is not in available countries"""

    def __init__(self, country: str, available_countries: list):
        self.country = country
        self.available_countries = available_countries
        self.message = f"{self.country} not in [{self.available_countries}]"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.country} -> {self.message}."


class InvalidOccupationValue(CocharError):
    """Raise when occupation is not in occupation list"""

    def __init__(self, occupation: str, available_occupations: list):
        self.occupation = occupation
        self.available_occupations = available_occupations
        self.message = f"{self.occupation} not in [{self.available_occupations}]"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidDamageBonusValue(CocharError):
    """Raise when occupation is not in occupation list"""

    def __init__(self, damage_bonus: str, correct_damage_bonus: list):
        self.damage_bonus = damage_bonus
        self.correct_damage_bonus = correct_damage_bonus
        self.message = f"{self.damage_bonus} not in [{self.correct_damage_bonus}]"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidBuildValue(CocharError):
    """Raise when occupation is not in occupation list"""

    def __init__(self, build: str, correct_build: list):
        self.build = build
        self.correct_build = correct_build
        self.message = f"{self.build} not in [{self.correct_build}]"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidOccupationEra(CocharError):
    """Raise when occupation era is not correct"""

    def __init__(self, era: str, correct_era: list):
        self.era = era
        self.correct_era = correct_era
        self.message = f"{self.era} not in [{self.correct_era}]"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidOccupationType(CocharError):
    """Raise when occupation type is not correct"""

    def __init__(self, _type: str, correct_type: list):
        self._type = _type
        self.correct_type = correct_type
        self.message = f"{self._type} not in [{self.correct_type}]"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidOccupationTags(CocharError):
    """Raise when tag is not among available tags"""

    def __init__(self, tags: str, correct_tags: list):
        self.tags = tags
        self.correct_tags = correct_tags
        self.message = f"{self.tags} not in [{self.correct_tags}]"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class NoneOccupationMeetsCriteria(CocharError):
    """Raise when searching criteria are not met by any occupation"""

    pass


class OccupationPointsBelowZero(CocharError):
    """Raise when provided occupation points are below 0"""

    pass
