"""
**Utilities for cochar module**

:param TRANSLATION_DICT: dictionary with translations for skills
:param AGE_RANGE: tuple[int, int], contains ranges of possible ages.
:param YEAR_RANGE: tuple[int], available years for last names

**legend**:

- a: art/craft
- s: science
- f: fighting
- g: firearms
- i: interpersonal
- l: language
- *: any

"""
from bisect import bisect_left
from typing import Dict, Tuple, Sequence

TRANSLATION_DICT: Dict[str, str] = {
    "a": "art/craft",
    "s": "science",
    "f": "fighting",
    "g": "firearms",
    "i": "interpersonal",
    "l": "language",
    "v": "survival",
    "p": "special",
    "*": None,
}

AGE_RANGE: Tuple[int, int] = (
    (15, 19),
    (20, 24),
    (25, 29),
    (30, 34),
    (35, 39),
    (40, 44),
    (45, 49),
    (50, 54),
    (55, 59),
    (60, 64),
    (65, 69),
    (70, 74),
    (75, 79),
    (80, 84),
    (85, 89),
    (90, 94),
    (95, 99),
)

YEAR_RANGE: Tuple[int] = (
    1950,
    1955,
    1960,
    1965,
    1970,
    1975,
    1980,
    1985,
    1990,
    1995,
    2000,
    2005,
    2010,
    2015,
    2020,
)


def narrowed_bisect(a: Sequence[int], x: int) -> int:
    """Standard bisect_left from bisect module
    can return number that exceed len(a).
    narrowed_bisect returns number that is <= len(a).

    It is to prevent IndexError, as many other variables
    relay on the index number returned.

    :param a: sequence of numbers
    :type a: Sequence
    :param x: number to insert
    :type x: int
    :return: position of insertion
    :rtype: int
    """
    i = bisect_left(a, x)
    return i if i != len(a) else i - 1


def is_skill_valid(skill_value: int) -> bool:
    """Check if skill value is int type and it is not
    below 0.

    :param skill_value: skill value to test
    :type skill_value: int
    :return: True if value is valid, else False
    :rtype: bool
    """
    if not isinstance(skill_value, int):
        return False
    if skill_value < 0:
        return False

    return True
