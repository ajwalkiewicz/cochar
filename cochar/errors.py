"""
**Errors for cochar module**

So far there is no plan to add custom errors for cochar module.
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
