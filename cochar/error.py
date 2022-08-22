"""
**Errors for cochar module**

TODO: Add more custom errors
"""


class SkillValueNotAnInt(Exception):
    """Skill value has to be an integer number"""

    pass


class SkillPointsBelowZero(Exception):
    """Skill points cannot be below zero"""

    pass


class SkillsNotADict(Exception):
    """Skills must be a dictionary"""

    pass
