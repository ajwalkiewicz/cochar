"""
Utilities

    legend:
    a - art/craft
    s -science
    f - fighting
    g - firearms
    i - interpersonal
    l - language
    * - any
    p - professor

    {
        "name": "",
        "credit_rating": [9, 50],
        "skills": []
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

CATEGORY_SKILLS_LIST: List [str] = [
    "language", "art/craft", "science", "fighting", "firearms"
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

YEAR_RANGE: Tuple[int] = (1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000,
              2005, 2010, 2015, 2020)


OCCUPATIONS_GROUPS: List[List[str]] = [
    [
        'antiquarian', 'clergy', 'librarian', 'journalist', 'engineer',
        'doctor of medicine', 'missionary', 'parapsychologist', 'author',
        'lawyer', 'professor'
    ],  # 1
    ['artist', 'zealot', 'musician'],  # 2
    [
        'artist', 'police detective', 'athlete', 'tribe member', 'farmer',
        'musician', 'police officer', 'military officer', 'pilot',
        'private investigator', 'criminal', 'drifter', 'soldier'
    ],  # 3
    ['dilettante', 'entertainer', 'zealot', 'drifter'],  # 4
    [
        'police detective', 'athlete', 'tribe member', 'farmer',
        'police officer', 'military officer', 'private investigator',
        'criminal', 'drifter', 'soldier',
        # 'test_occ'
    ]
]  # 5

OCCUPATIONS_LIST: List[str] = [
    'antiquarian',
    'artist',
    'athlete',
    'author',
    'clergy',
    'criminal',
    'dilettante',
    'doctor of medicine',
    'drifter',
    'engineer',
    'entertainer',
    'farmer',
    'journalist',
    'lawyer',
    'librarian',
    'military officer',
    'missionary',
    'musician',
    'parapsychologist',
    'pilot',
    'police detective',
    'police officer',
    'private investigator',
    'professor',
    'soldier',
    'tribe member',
    'zealot',
    # 'test_occ'
]

OCCUPATIONS_DATA: Dict[str, Dict[str, List[Union[int, str]]]] = {
    "antiquarian": {
        "credit_rating": [30, 70],
        "skills": ['appraise', 'history', 'library use', 'spot hidden']
    },
    "artist": {
        "credit_rating": [9, 50],
        "skills":
        ["psychology", "spot hidden", (1, "history", "natural world")]
    },
    "athlete": {
        "credit_rating": [9, 70],
        "skills": ["climb", "jump", "brawl", "ride", "swim", "throw", "1i"]
    },
    "author": {
        "credit_rating": [9, 30],
        "skills": [
            "art/craft (literature)", "language (own)",
            "psychology", "library use", "history",
            (1, "occult", "natural world"), "1l", "1*"
        ]
    },
    "entertainer": {
        "credit_rating": [9, 30],
        "skills": ["acting", "disguise", "listen", "psychology", "2i", "2*"]
    },
    "soldier": {
        "credit_rating": [9, 30],
        "skills": [
            "doge", "stealth", "survival", (1, "climb", "swim"),
            (2, "first aid", "mechanical repair", "1l"), "1f", "1g", "1l"
        ]
    },
    "lawyer": {
        "credit_rating": [30, 80],
        "skills":
        ["accounting", "law", "library use", "psychology", "2i", "2*"]
    },
    "librarian": {
        "credit_rating": [9, 35],
        "skills": ["accounting", "library use", "language (own)", "1l", "4*"]
    },
    "military officer": {
        "credit_rating": [20, 70],
        "skills": [
            "accounting", "firearms", "navigate", "psychology", "survival",
            "2i", "1*"
        ]
    },
    "missionary": {
        "credit_rating": [0, 30],
        "skills": [
            "first aid", "mechanical repair", "medicine", "natural world",
            "1a", "1i", "2*"
        ]
    },
    "musician": {
        "credit_rating": [9, 30],
        "skills":
        ["art/craft (instrument)", "listen", "psychology", "1a", "1i", "4*"]
    },
    "parapsychologist": {
        "credit_rating": [9, 30],
        "skills": [
            "art/craft (photography)", "anthropology", "history",
            "library use", "occult", "psychology", "1l", "1*"
        ]
    },
    "pilot": {
        "credit_rating": [20, 70],
        "skills": [
            "electrical repair", "mechanical repair", "navigate",
            "operate heavy machinery", "pilot (aircraft)",
            "science (astronomy)", "2*"
        ]
    },
    "clergy": {
        "credit_rating": [9, 60],
        "skills": [
            "accounting", "history", "library use", "listen", "psychology",
            "1i", "1l", "1*"
        ]
    },
    "criminal": {
        "credit_rating": [5, 65],
        "skills": [
            "psychology", "spot hidden", "stealth",
            (4, "appraise", "disguise", "fighting", "firearms", "locksmith",
             "mechanical repair", "sleight of hand"), "1i"
        ]
    },
    "dilettante": {
        "credit_rating": [50, 99],
        "skills": ["ride", "firearms", "1a", "1i", "1l", "3*"]
    },
    "doctor of medicine": {
        "credit_rating": [30, 80],
        "skills": [
            "first aid", "language (latin)", "medicine", "psychology",
            "science (biology)", "science (pharmacy)", "2*"
        ]
    },
    "drifter": {
        "credit_rating": [0, 5],
        "skills": ["climb", "jump", "navigate", "1i", "2*"]
    },
    "engineer": {
        "credit_rating": [30, 60],
        "skills": [
            "art/craft (technical drawing)", "electrical repair",
            "library use", "mechanical repair", "operate heavy machinery",
            "science (engineering)", "science (physics)", "1*"
        ]
    },
    "farmer": {
        "credit_rating": [9, 30],
        "skills": [
            "art/craft (farming)", "drive auto", "1i", "mechanical repair",
            "natural world", "operate heavy machinery", "track", "1*"
        ]
    },
    "hacker": {
        "credit_rating": [10, 70],
        "skills": [
            "computer use", "electrical repair", "electronics", "library use",
            "spot hidden", "1i", "2*"
        ]
    },
    "journalist": {
        "credit_rating": [9, 30],
        "skills": [
            "art/craft (photography)", "history", "library use",
            "language (own)", "1i", "psychology", "2*"
        ]
    },
    "police detective": {
        "credit_rating": [20, 50],
        "skills": [
            "firearms", "law", "listen", "psychology", "spot hidden",
            (1, "art/craft (acting)", "disguise"), "1i", "1*"
        ]
    },
    "police officer": {
        "credit_rating": [9, 30],
        "skills": [
            "fighting (brawl)", "firearms", "first aid", "law", "psychology", "spot hidden",
            (1, "drive auto", "ride"), "1i"
        ]
    },
    "private investigator": {
        "credit_rating": [9, 30],
        "skills": [
            "art/craft (photography)", "disguise", "law", "library use", "1i",
            "psychology", "spot hidden", "1*"
        ]
    },
    "professor": {
        "credit_rating": [20, 70],
        "skills": ["library use", "1l", "language (own)", "psychology", "4p"]
    },
    "tribe member": {
        "credit_rating": [0, 15],
        "skills": [
            "climb", "fighting", "throw", "natural world", "listen", "occult",
            "spot hidden", "swim", "survival (any)"
        ]
    },
    "zealot": {
        "credit_rating": [0, 30],
        "skills": ["history", "psychology", "stealth", "2i", "3*"]
    },
    "test_occ": {
        "credit_rating": [1, 99],
        "skills": [
            "history",
            "psychology",
            "stealth",
            # "listen", "psychology",
            # (2, "first aid", "mechanical repair", "1l"), "2a", "2s", "2f",
            # "2g", "2i", "2l", "2*"
        ]
    },
}

# Credit ratin is not in a default basic skills
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
    "track": 10
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
        "art/craft (instrument)": 5
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
        "science (zoology)": 1
    },
    "fighting": {
        "fighting (axe)": 15,
        "fighting (brawl)": 25,
        "fighting (chainsaw)": 10,
        "fighting (flail)": 10,
        "fighting (garrote)": 15,
        "fighting (sword)": 20,
        "fighting (whip)": 5
    },
    "firearms": {
        "firearms (bow)": 15,
        "firearms (handgun)": 20,
        "firearms (heavy wepons)": 10,
        "firearms (machine gun)": 10,
        "firearms (rifle)": 25,
        "firearms (shotgun)": 25,
        "firearms (spear)": 20,
        "firearms (submachine gun)": 15
    },
    "interpersonal": {
        "fast talk": 5,
        "intimidate": 15,
        "persuade": 10,
        "psychology": 10
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
        "anthropology": 1
    }
}

# Creating ALL_SKILLS dictionary
ALL_SKILLS: Dict[str, int] = {}
ALL_SKILLS.update(BASIC_SKILLS)

for category in CATEGORY_SKILLS.keys():
    ALL_SKILLS.update(CATEGORY_SKILLS[category])