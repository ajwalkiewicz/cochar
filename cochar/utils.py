"""
**Utilities for cochar module**

:param TRANSLATION_DICT: dictionary with translations for skills
:param CATEGORY_SKILLS_LIST: 
:param AGE_RANGE: tuple[int, int], contains ranges of possible ages.
:param YEAR_RANGE: tupel[int], available years for last names
:param OCCUPATIONS_GROUPS: list[list[str]], list of 5 occupation groups.
:param OCCUPATIONS_LIST: list of all occupations
:param OCCUPATIONS_DATA: dictionary with occupation details
:param BASIC_SKILLS: dictionary with basic skills data
:param CATEGORY_SKILLS: dictionary with skills divided on cathegories
:param ALL_SKILLS: dict with all skills

**legend**:

- a: art/craft
- s: science
- f: fighting
- g: firearms
- i: interpersonal
- l: language
- \*: any
- p: professor

**Occupation template**

.. code-block:: python
    :linenos:

     OCCUPATION_DATA = {
        "occupation name": {
            "credit_rating": [9, 50],
            "skills": []
        }
    }

"""
from typing import Dict, List, Tuple, Union

TRANSLATION_DICT: Dict[str, str] = {
    "a": "art/craft",
    "s": "science",
    "f": "fighting",
    "g": "firearms",
    "i": "interpersonal",
    "l": "language",
    "*": None,
    "p": "professor"
    # just for professor occ. (i ingored doctor, and give him 2*)
}

CATEGORY_SKILLS_LIST: List[str] = [
    "language",
    "art/craft",
    "science",
    "fighting",
    "firearms",
]

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

# Credit raiting is not in a default basic skills
BASIC_SKILLS: Dict[str, int] = {
    "accounting": 5,
    "acting": 5,
    "anthropology": 1,
    "appraise": 5,
    "archaeology": 1,
    "art/craft": 1,  # art/craft
    "charm": 15,
    "climb": 20,
    "disguise": 5,
    "doge": 0,  # to check
    "drive auto": 20,
    "electrical repair": 10,
    "fast talk": 5,
    "fighting": 1,
    "fighting brawl": 25,
    "firearms": 1,
    "firearms (handgun)": 20,
    "firearms (rifle shotgun)": 25,
    "first aid": 30,
    "history": 5,
    "intimidate": 15,
    "jump": 20,
    "language": 1,
    "language (own)": 0,  # To check
    "law": 5,
    "library use": 20,
    "listen": 20,
    "locksmith": 1,
    "mechanical repair": 10,
    "medicine": 1,
    "natural world": 10,
    "navigate": 10,
    "occult": 5,
    "operate heavy machinery": 1,
    "persuade": 10,
    "pilot": 1,
    "psychoanalysis": 1,
    "psychology": 10,
    "ride": 5,
    "science": 1,  # science
    "sleight of hand": 10,
    "spot hidden": 25,
    "stealth": 20,
    "survival": 10,
    "swim": 20,
    "throw": 20,
    "track": 10,
}

CATEGORY_SKILLS: Dict[str, Dict[str, int]] = {
    "art/craft": {
        "art/craft (acting)": 5,
        "art/craft (barber)": 5,
        "art/craft (calligraphy)": 5,
        "art/craft (cook)": 5,
        "art/craft (dancer)": 5,
        "art/craft (fine art)": 5,
        "art/craft (forgery)": 5,
        "art/craft (literature)": 5,
        "art/craft (writer)": 5,
        "art/craft (morris dancer)": 5,
        "art/craft (opera singer)": 5,
        "art/craft (painter and decorator)": 5,
        "art/craft (photography)": 5,
        "art/craft (potter)": 5,
        "art/craft (sculptor)": 5,
        "art/craft (vacume tube blower)": 5,
        "art/craft (instrument)": 5,
    },
    "science": {
        "science (astronomy)": 1,
        "science (biology)": 1,
        "science (botany)": 1,
        "science (chemistry)": 1,
        "science (cryptography)": 1,
        "science (forensics)": 1,
        "science (geology)": 1,
        "science (mathematics)": 1,
        "science (meteorology)": 1,
        "science (pharmacy)": 1,
        "science (physics)": 1,
        "science (zoology)": 1,
    },
    "fighting": {
        "fighting (axe)": 15,
        "fighting (brawl)": 25,
        "fighting (chainsaw)": 10,
        "fighting (flail)": 10,
        "fighting (garrote)": 15,
        "fighting (sword)": 20,
        "fighting (whip)": 5,
    },
    "firearms": {
        "firearms (bow)": 15,
        "firearms (handgun)": 20,
        "firearms (heavy wepons)": 10,
        "firearms (machine gun)": 10,
        "firearms (rifle)": 25,
        "firearms (shotgun)": 25,
        "firearms (spear)": 20,
        "firearms (submachine gun)": 15,
    },
    "interpersonal": {
        "fast talk": 5,
        "intimidate": 15,
        "persuade": 10,
        "psychology": 10,
    },
    "language": {
        "language (own)": 0,
        "language (german)": 0,
        "language (spanish)": 0,
        "language (french)": 0,
        "language (latin)": 0,
        "language (acient greek)": 0,
        "language (egiptian)": 0,
        "language (other)": 0,
    },
    # "modern": {
    #     "computer use": 5,
    #     "electronics": 1
    # },
    # "extra": {
    #     "cthulhu mythos": 0
    # }
    "professor": {
        "language (own)": 0,
        "language (german)": 0,
        "language (spanish)": 0,
        "language (french)": 0,
        "language (latin)": 0,
        "language (acient greek)": 0,
        "language (egiptian)": 0,
        "language (other)": 0,
        "psychology": 10,
        "science (astronomy)": 1,
        "science (biology)": 1,
        "science (botany)": 1,
        "science (chemistry)": 1,
        "science (cryptography)": 1,
        "science (forensics)": 1,
        "science (geology)": 1,
        "science (mathematics)": 1,
        "science (meteorology)": 1,
        "science (pharmacy)": 1,
        "science (physics)": 1,
        "science (zoology)": 1,
        "psychoanalysis": 1,
        "medicine": 1,
        "occult": 5,
        "anthropology": 1,
    },
}

# Creating ALL_SKILLS dictionary
ALL_SKILLS: Dict[str, int] = {}
ALL_SKILLS.update(BASIC_SKILLS)

for category in CATEGORY_SKILLS.keys():
    ALL_SKILLS.update(CATEGORY_SKILLS[category])
