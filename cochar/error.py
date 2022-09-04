"""
**Errors for cochar module**

TODO: Add more custom errors
"""
from typing import Any


class CocharError(Exception):
    pass


class CharacteristicValueNotAnInt(CocharError):
    """Characteristic value has to be an integer number"""

    def __init__(self, skill_name: str, skill_value: Any):
        self.skill_name = skill_name
        self.skill_value = skill_value
        self.message = f"{self.skill_name.capitalize()} points must be an integer: '{self.skill_value}'"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class CharacteristicPointsBelowZero(CocharError):
    """Characteristic points cannot be below zero"""

    def __init__(self, skill_name: str):
        self.skill_name = skill_name
        self.message = f"'{self.skill_name}' Characteristic points cannot be below zero"
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
        self.message = f"'{self.skill}' Skills must be an dictionary"
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidYearValue(CocharError):
    """Year must be an integer number"""

    def __init__(self, year: int):
        self.year = year
        self.message = f"'{self.year}' Year must be an integer number"
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
