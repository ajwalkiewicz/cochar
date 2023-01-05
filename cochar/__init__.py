# __init__.py
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Union, Set

import randname

__title__ = "cochar"
__version__ = "1.0.0-alpha.5"
__author__ = "Adam Walkiewicz"
__license__ = "GPL 3.0"

DEFAULT_LOGGING_LEVEL = logging.ERROR

LOGGING_LEVEL_MAP = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
}

logging_level = DEFAULT_LOGGING_LEVEL

logging.basicConfig(
    format="[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s",
    level=logging_level,
)


def set_logging_level(logging_level=logging_level):
    logging_level = LOGGING_LEVEL_MAP.get(logging_level)
    return logging.basicConfig(
        format="[%(asctime)s][%(levelname)s][%(filename)s:%(funcName)s:%(lineno)d] %(message)s",
        level=logging_level,
    )


SEX_OPTIONS: Set[Union[str, bool]] = {"M", "m", "F", "f", None}
_THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
POP_PYRAMID_PATH = os.path.abspath(
    os.path.join(_THIS_FOLDER, "data", "popPyramid.json")
)

# modification's table for characteristics:
MODIFIERS = {
    "age_range": [19, 39, 49, 59, 69, 79, 90],
    "mod_char_points": [5, 0, 5, 10, 20, 40, 80],
    "mod_app": [0, 0, 5, 10, 15, 20, 25],
    "mod_move_rate": [0, 0, 1, 2, 3, 4, 5],
    "mod_edu": [0, 1, 2, 3, 4, 4, 4],
}
# Value matrix for setting build
VALUE_MATRIX = {
    "combat_range": [64, 84, 124, 164, 204, 283, 364, 444, 524],
    "build": [-2, -1, 0, 1, 2, 3, 4, 5, 6],
    "damage_bonus": ["-2", "-1", "0", "+1K4", "+1K6", "+2K6", "+3K6", "+4K6", "+5K6"],
}

with open(
    os.path.join(_THIS_FOLDER, "data", "occupations.json"), "r", encoding="utf-8"
) as json_file:
    # Full data of occupations
    OCCUPATIONS_DATA: Dict[str, dict] = dict(json.load(json_file))
    # OCCUPATIONS_DATA.pop("test")
    # Just occupations names in the list
    OCCUPATIONS_LIST: List[str] = list(OCCUPATIONS_DATA.keys())
    # Occupations divided on 5 categories depends on skill point calculation method
    OCCUPATIONS_GROUPS: List[List[str]] = [
        [key for key, value in OCCUPATIONS_DATA.items() if "edu" in value["groups"]],
        [key for key, value in OCCUPATIONS_DATA.items() if "edupow" in value["groups"]],
        [key for key, value in OCCUPATIONS_DATA.items() if "edudex" in value["groups"]],
        [key for key, value in OCCUPATIONS_DATA.items() if "eduapp" in value["groups"]],
        [key for key, value in OCCUPATIONS_DATA.items() if "edustr" in value["groups"]],
    ]

with open(
    os.path.join(_THIS_FOLDER, "data", "settings.json"), "r", encoding="utf-8"
) as json_file:
    settings: dict = json.load(json_file)
    MIN_AGE: int = settings["min_age"]
    MAX_AGE: int = settings["max_age"]
    MAX_SKILL_LEVEL: int = settings["max_skill_level"]
    YEAR: int = settings["year"]
    AGE: int = settings["age"]
    SEX: str = settings["sex"]
    FIRST_NAME: str = settings["first_name"]
    LAST_NAME: str = settings["last_name"]
    COUNTRY: str = settings["country"]
    OCCUPATION: str = settings["occupation"]
    WEIGHTS: bool = settings["weights"]
    SHOW_WARNINGS: bool = settings["show_warnings"]
    OCCUPATION_TYPE: str = settings["occupation_type"]
    ERA: str = settings["era"]
    TAGS: List[str] = settings["tags"]

    DATABASE: str = settings["database"]
    if not DATABASE:
        DATABASE = randname.DATABASE

SKILLS_DATABASE = Path() / _THIS_FOLDER / "data" / "skills.json"

from cochar.cochar import *
