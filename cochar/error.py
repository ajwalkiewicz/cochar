"""
**Errors for cochar module**

TODO: Add more custom errors
"""


class CocharError(Exception):
    pass


class SkillValueNotAnInt(CocharError):
    """Skill value has to be an integer number"""

    pass


class SkillPointsBelowZero(CocharError):
    """Skill points cannot be below zero"""

    pass


class SkillsNotADict(CocharError):
    """Skills must be a dictionary"""

    pass
