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
