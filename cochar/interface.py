# Cochar - create a random character for Call of Cthulhu RPG 7th ed.
# Copyright (C) 2023  Adam Walkiewicz

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from typing import List, Dict

import os
import json
import itertools


class SkillsDataInterface(ABC):
    def __init__(self, database: Path, era: str):
        self.database = database
        self.era = era

    @abstractmethod
    def get_skills(self) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_skills_from_category(self) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_all_skills_names(self) -> List[str]:
        pass

    @abstractmethod
    def get_categories_names(self) -> List[str]:
        pass

    @abstractmethod
    def get_basic_skills_names(self) -> List[str]:
        pass


class SkillsJSONInterface(SkillsDataInterface):
    def __init__(self, database: Path, era: set = None):
        super().__init__(database, era)
        self.load_data(database)
        self.database = database
        if not era:
            self.era = {"classic-1920", "modern"}
        else:
            self.era = set(era)

    def load_data(self, database) -> None:
        with open(database, "r", encoding="utf-8") as json_file:
            self.skills_data: Dict = json.load(json_file)

    def get_skills(self) -> Dict[str, int]:
        return {
            skill: item["value"]
            for skill, item in self.skills_data.items()
            if set(item["era"]).issuperset(self.era)
        }

    def get_all_skills_names(self) -> List[str]:
        return [
            skill
            for skill, item in self.skills_data.items()
            if set(item["era"]).issuperset(self.era)
        ]

    # TODO: filter out categories that are not in current era
    def get_categories_names(self) -> List[str]:
        return list(
            set(
                itertools.chain(
                    *map(lambda item: item["categories"], self.skills_data.values())
                )
            )
        )

    def get_basic_skills_names(self) -> List:
        skills_basic = [
            skill
            for skill, item in self.skills_data.items()
            if "basic" in self.skills_data[skill]["categories"]
            and set(item["era"]).issuperset(self.era)
        ]
        return skills_basic

    def get_skills_from_category(self, category) -> List[str]:
        return [
            skill
            for skill, item in self.skills_data.items()
            if category in self.skills_data[skill]["categories"]
            and set(item["era"]).issuperset(self.era)
        ]


class SkillsSQLInterface(SkillsDataInterface):
    # TODO: implement SQL interface
    pass


class SkillsRedisInterface(SkillsDataInterface):
    # TODO: implement Redis interface
    pass
