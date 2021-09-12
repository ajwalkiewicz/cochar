#!/usr/bin/python3
"""Call of Cthulhu character generator

Example:

>>> Character()
"""
import random
import os
import json
import randname
from typing import Dict, List, Tuple, Union
from bisect import bisect_left
from .utils import OCCUPATIONS_GROUPS, OCCUPATIONS_LIST
from .utils import OCCUPATIONS_DATA
from .utils import BASIC_SKILLS
from .utils import ALL_SKILLS
from .utils import CATEGORY_SKILLS
from .utils import TRANSLATION_DICT
from .utils import CATEGORY_SKILLS_LIST
from .utils import AGE_RANGE
from .utils import YEAR_RANGE
# from .utils import *

_THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
POP_PIRAMID_PATH = os.path.abspath(os.path.join(_THIS_FOLDER, 'data', 'popPiramid.json'))


class Character():
    _MIN_AGE: int = 15
    _MAX_AGE: int = 90
    __SEX_OPTIONS: list = ['M', 'F', None]
    OCCUPATIONS_GROUPS: list = OCCUPATIONS_GROUPS.copy()
    OCCUPATIONS_LIST: list = OCCUPATIONS_LIST.copy()
    max_skill_level: int = 90

    def __init__(
            self,
            year: int = 1925,
            age: str = None,
            sex: str = None,
            first_name: str = None,
            last_name: str = None,
            country: str = "US",
            occupation: str = "optimal",
            # occupation_mode: str = "optimal",
            weights: bool = True) -> None:
            # add skills (for repr)
        self._year: int = year
        if sex in self.__SEX_OPTIONS:
            self._sex = self.set_sex(sex)
        else:
            raise ValueError("incorrect sex falue: sex -> ['M', 'F', None']") 
        self._age: int = self.set_age(age)
        self._country: str = country
        self._weights: bool = weights
        # personals
        self._first_name: str = randname.first_name(self._year, self._sex, self._country, self._weights) if not first_name else first_name
        self._last_name: str = randname.first_name(self._year, self._sex, self._country, self._weights) if not last_name else last_name
        # characteristics
        self._characteristics: dict[str, int] = {}
        self._str: int = 0
        self._con: int = 0
        self._siz: int = 0
        self._dex: int = 0
        self._app: int = 0
        self._edu: int = 0
        self._int: int = 0
        self._pow: int = 0
        self._move_rate: int = 0
        self.set_characteristics()
        # derived atributes
        self._sanity_points: int = 0
        self._magic_points: int = 0
        self._hit_points: int = 0
        self._luck: int = 0
        self._set_derived_attributes()
        # occupation
        if occupation in self.OCCUPATIONS_LIST + ["optimal", "random", None]:
            self._occupation = occupation
        else:
            raise ValueError("occupation incorrect")
        
        # if occupation_mode in ["optimal", "random"]:
        #     self._occupation_mode = "optimal"
        # else:
        #     raise ValueError("incorrect occupation mode")
        
        self.skill_points_groups: tuple[int] = (
            self._edu * 4,                  # 1
            self._edu * 2 + self._pow * 2,  # 2
            self._edu * 2 + self._dex * 2,  # 3
            self._edu * 2 + self._app * 2,  # 4
            self._edu * 2 + self._str * 2,  # 5
        )

        self._occupation: str = self.set_occupation(self._occupation)
        self._occupation_points: int = self.get_skill_points(self._occupation)
        self._hobby_points: int = self._int * 2 # Create public function for that

        # Skills
        self._skills: dict[str, int] = {}
        self.occupation_skills_list: list[str] = []
        self.hobby_skills_list: list[str] = []

        ALL_SKILLS.update({"doge": self._dex // 2, "language (own)": self._edu})
        self._skills: dict = self.set_skills_dict()

        # credit rating
        # assigning points to credit rating
        credit_rating_points: int = random.randint(
            *OCCUPATIONS_DATA[self._occupation]['credit_rating'].copy())
        self._occupation_points -= credit_rating_points
        self._skills.setdefault('credit rating', credit_rating_points)

        # combat values
        self._damage_bonus: str = ""
        self._build: int = 0
        self._doge: int = 0
        self.set_combat_values()

    @property
    def year(self) -> int:
        return self._year
    
    @property
    def sex(self) -> Union[str, None]:
        return self._sex
    
    @property
    def age(self) -> int:
        return self._age

    @property
    def country(self) -> str:
        return self._country
    
    @property
    def weights(self) -> bool:
        return self._weights

    @property
    def occupation(self) -> str:
        return self._occupation

    @property
    def characteristics(self) -> dict:
        return self._characteristics

    @property
    def strength(self) -> int:
        return self._str

    @property
    def condition(self) -> int:
        return self._con

    @property
    def size(self) -> int:
        return self._siz

    @property
    def dexterity(self) -> int:
        return self._dex

    @property
    def apperance(self) -> int:
        return self._app

    @property
    def edducation(self) -> int:
        return self._edu

    @property
    def intelligence(self) -> int:
        return self._int

    @property
    def power(self) -> int:
        return self._pow

    @property
    def move_rate(self) -> int:
        return self._move_rate

    # add property for name
    # and characteristics
    # and skills

    @strength.setter
    def strength(self, new_strength: int) -> int:
        try:
            int(new_strength)
        except ValueError:
            raise ValueError("Invalid strength. Strength must me an integer")
        if new_strength < 0:
            raise ValueError("Strength cannot be less than 0")
        self._str = new_strength

    @condition.setter
    def condition(self, new_condition: int) -> int:
        try:
            int(new_condition)
        except ValueError:
            raise ValueError("Invalid condition. Strength must me an integer")
        if new_condition < 0:
            raise ValueError("Strength cannot be less than 0")
        self._con = new_condition


    @year.setter
    def year(self, new_year: int) -> int:
        try:
            int(new_year)
            self._year = new_year
        except ValueError:
            raise ValueError("invalid year. year must be integer")

    @sex.setter
    def sex(self, new_sex: Union[str, None]) -> Union[str, None]:
        if new_sex in ['M', 'F', None]:
            self._sex = self.set_sex(new_sex)
        else:
            raise ValueError("incorrect sex falue: sex -> ['M', 'F', None']")

    @age.setter
    def age(self, new_age: int) -> int:
        if self._MIN_AGE <= new_age <= self._MAX_AGE:
            self._age = new_age
        else:
            raise ValueError(f"age not in range: [{self._MIN_AGE}, {self._MAX_AGE}]")

    @country.setter
    def country(self, new_country: str) -> str:
        # TO DO
        self._country = new_country

    @weights.setter
    def weights(self, new_weights: bool) -> bool:
        if isinstance(new_weights, bool):
            self._weights = new_weights
        else:
            raise ValueError("weights must be a bool")

    @occupation.setter
    def occupation(self, new_occupation: str) -> str:
        # TO DO
        self._occupation = new_occupation
    
    @staticmethod
    def set_sex(sex: Union[str, None]) -> str:
        if sex is None:
            return random.choice(['M', 'F'])
        else:
            return sex.upper()

    def set_age(self, age: int = None) -> int:
        """Set age  

        :param age: new age, defaults to None
        :type age: int, optional
        :return: new age
        :rtype: int
        """
        if age is None:
            variable_year = self._year
            if variable_year < 1950:
                variable_year = 1950
            else:
                year_index = bisect_left(YEAR_RANGE, self._year)
                variable_year = YEAR_RANGE[year_index]
            variable_name = f'pop{variable_year}'

            with open(POP_PIRAMID_PATH) as json_file:
                age_population = AGE_RANGE
                age_weights = json.load(json_file)[variable_name][
                    self._sex][3:-1]
                age_range = random.choices(age_population,
                                           weights=age_weights)[0]
                self._age = random.randint(*age_range)
            return self._age
        else:
            self._age = age
            return self._age

    ###################### CHARACTERISTICS ########################

    def set_characteristics(self) -> Dict[str, int]:
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        # Main characteristics
        self._str = random.randint(15, 90)
        self._con = random.randint(15, 90)
        self._siz = random.randint(40, 90)
        self._dex = random.randint(15, 90)
        self._app = random.randint(15, 90)
        self._edu = random.randint(40, 90)
        self._int = random.randint(40, 90)
        self._pow = random.randint(15, 90)
        self._move_rate = 0

        # Modificators table for characteristics depends on age
        MODIFIERS = {
            'age_range': [19, 39, 49, 59, 69, 79, 90],
            'mod_char_points': [5, 0, 5, 10, 20, 40, 80],
            'mod_app': [0, 0, 5, 10, 15, 20, 25],
            'mod_move_rate': [0, 0, 1, 2, 3, 4, 5],
            'mod_edu': [0, 1, 2, 3, 4, 4, 4]
        }

        age_range = bisect_left(MODIFIERS['age_range'], self.age)
        mod_char_points = MODIFIERS['mod_char_points'][age_range]
        mod_app = MODIFIERS['mod_app'][age_range]
        mod_move_rate = MODIFIERS['mod_move_rate'][age_range]
        mod_edu = MODIFIERS['mod_edu'][age_range]

        self._substract_characteristics_points(mod_points=mod_char_points,
                                               char='_app',
                                               points=mod_app)

        self._characteristic_test('_edu', mod_edu)
        self._correct_move_rate(mod_move_rate)

        self._characteristics: dict[str, int] = {
            "str": self._str,
            "con": self._con,
            "siz": self._siz,
            "dex": self._dex,
            "app": self._app,
            "edu": self._edu,
            "int": self._int,
            "pow": self._pow,
            "move_rate": self._move_rate,
        }

        return self._characteristics

    def _set_derived_attributes(self) -> None:
        # Warning! First use add_characteristics method
        self._sanity_points = self._pow
        self._magic_points = self._pow // 5
        self._hit_points = (self._siz + self._con) // 10
        self._luck = random.randint(15, 90)

        if self.age <= 19:
            self._luck = max(self._luck, random.randint(15, 90))

    def _substract_characteristics_points(self, mod_points: int = None, char: str = '', points: int = 0) -> None:
        if char and points:
            setattr(self, char, getattr(self, char) - points)

            if getattr(self, char) < 1:
                setattr(self, char, 1)

        if mod_points:
            for _ in range(mod_points):
                choice = [
                    skill for skill in ('_str', '_con', '_dex')
                    if getattr(self, skill) != 1
                ]
                if choice:
                    skill = random.choice(choice)
                    setattr(self, skill, getattr(self, skill) - 1)
                else:
                    break

    def _characteristic_test(self, attr_name: str, count: int) -> None:
        characteristic_value = getattr(self, attr_name)
        for _ in range(count):
            test = random.randint(1, 100)
            if characteristic_value < test:
                characteristic_value += random.randint(1, 10)
        setattr(self, attr_name, characteristic_value)

    def _correct_move_rate(self, count: int) -> None:
        if self._dex < self._siz and self._str < self._siz:
            self._move_rate = 7
        elif self._str >= self._siz and self._dex >= self._siz:
            self._move_rate = 9
        else:
            self._move_rate = 8

        self._move_rate -= count


    ########################## OCCUPATION ###########################

    def set_occupation(self, occupation: str) -> str:
        """[summary]

        :param occupation: [description]
        :type occupation: [type]
        :return: [description]
        :rtype: [type]
        """
        if occupation == 'random':
            self._occupation = random.choice(self.occupations_list)
            return self._occupation
        elif occupation == 'optimal':
            skill_points = max(self.skill_points_groups)
            occupations = random.choice([
                group for index, group in enumerate(self.OCCUPATIONS_GROUPS)
                if self.skill_points_groups[index] == skill_points
            ])
            self._occupation = random.choice(occupations)
            return self._occupation
        else:
            self._occupation = occupation
            return self._occupation

    ########################### SKILLS #####################3########

    def get_skill_points(self, occupation: str) -> int:
        """[summary]

        :param occupation: [description]
        :type occupation: str
        :return: [description]
        :rtype: [type]
        """
        group_index = [
            index for index, group in enumerate(self.OCCUPATIONS_GROUPS) if occupation in group
        ]
        points = [self.skill_points_groups[i] for i in group_index]

        return max(points)

    def set_skills_dict(self):
        """[summary]

        :return: [description]
        :rtype: [type]
        """
        self._skills = {}
        occupation_input_list = OCCUPATIONS_DATA[
            self._occupation]["skills"].copy()
        self.occupation_skills_list = self._get_skills_list(
            occupation_input_list)

        # categories = [f"1{cat}" for cat in TRANSLATION_DICT.keys()]
        # hobby_input_list = list(BASIC_SKILLS.keys()) + categories
        hobby_input_list = list(BASIC_SKILLS.keys())
        self.hobby_skills_list = self._get_skills_list(hobby_input_list)

        self._assign_skill_points(self._occupation_points,
                                  self.occupation_skills_list)
        self._assign_skill_points(self._hobby_points, self.hobby_skills_list)
        self._skills = self.filter_skills(self._skills)
        
        return self._skills

    def _get_skills_list(self, input_list: list) -> List[str]:
        skills_list = []
        skills_list += list(
            filter(
                lambda x: len(x) > 2 and isinstance(x, str) and x not in
                CATEGORY_SKILLS_LIST, input_list))
        skills_list += self._get_choice_skills(input_list)
        skills_list += self._get_category_skills(input_list)
        return skills_list

    def _get_choice_skills(self, skills_list: list) -> List[str]:
        result = []
        for item in skills_list:
            if isinstance(item, tuple):
                population = item[1:]
                k = item[0]
                result.extend(random.choices(population, k=k))
                result.extend(self._get_category_skills(result))
                result = list(filter(lambda x: len(x) > 2, result))
        return result

    def _get_category_skills(self, skills_list: list) -> List[str]:
        result = []
        for item in skills_list:
            if len(item) == 2:
                k = int(item[0])
                if item[1] == "*":
                    population = list(BASIC_SKILLS.keys())
                else:
                    population = list(CATEGORY_SKILLS[TRANSLATION_DICT.get(
                        item[1])].keys())
                result.extend(random.choices(population, k=k))

            elif item in CATEGORY_SKILLS_LIST:
                population = list(CATEGORY_SKILLS[item].keys())
                result.extend([random.choice(population)])

        return result

    def _assign_skill_points(self, points: int, skills_list: list) -> None:
        for skill in skills_list:
            if skill in ALL_SKILLS:
                self._skills.setdefault(skill, ALL_SKILLS[skill])
            else:
                self._skills.setdefault(skill, 1)

        while points:
            skill = random.choice(skills_list)
            if points <= self.max_skill_level - self._skills[skill]:
                points_allocation = random.randint(0, points)
            elif sum(list(self._skills.values())) % 90 == 0:
                break
            elif self._skills[skill] >= self.max_skill_level:
                continue
            else:
                points_allocation = random.randint(
                    0, self.max_skill_level - self._skills[skill])
            self._skills[skill] += points_allocation
            points -= points_allocation

    def filter_skills(self, _skills: dict) -> Dict[str, int]:
        """Filter out all skills with basic value form given dict.

        >>> example_dict = {'psychoanalysis': 1, 'language (spanish)': 66}
        >>> filter_skills(example_dict)
        {'language (spanish)': 66}
        """
        return dict(
            filter(
                lambda item: ALL_SKILLS.get(item[
                    0], ALL_SKILLS.setdefault(item[0], 1)) != item[1],
                _skills.items()))

    ######################## COMBAT VALUES #############################

    def set_combat_values(self) -> None:
        VALUE_MATRIX = {
            'combat_range': [64, 84, 124, 164, 204, 283, 364, 444, 524],
            'damage_bonus':
            ['-2', '-1', '0', '+1K4', '+1K6', '+2K6', '+3K6', '+4K6', '+5K6'],
            'build': [-2, -1, 0, 1, 2, 3, 4, 5, 6]
        }

        sum_str_siz = self._str + self._siz
        combat_range = bisect_left(VALUE_MATRIX['combat_range'], sum_str_siz)
        self._damage_bonus = VALUE_MATRIX['damage_bonus'][combat_range]
        self._build = VALUE_MATRIX['build'][combat_range]

        # self._doge = self._dex // 2 if self._doge == 0 else self._doge

        if self._doge == 0:
            self._doge = self._dex // 2


    def __str__(self) -> str:
        return f"""
        Character:
            "personals":
                "name": "{self._first_name} {self._last_name}",
                "occupation": {self._occupation.capitalize()},
                "age": {self._age},
                "sex": {self._sex.upper()},
            "characteristics":
                "str": {self._str},
                "con": {self._con},
                "siz": {self._siz},
                "dex": {self._dex},
                "app": {self._app},
                "edu": {self._edu},
                "int": {self._int},
                "pow": {self._pow},
                "move_rate": {self._move_rate},
            "hit_points": {self._hit_points},
            "sanity": {self._sanity_points},
            "luck": {self._luck},
            "magic_points": {self._magic_points},
            "combat":
                "damage bonus": {self._damage_bonus},
                "build": {self._build},
                "doge": {self._doge},
            "skills": {self._skills},
        """

    def __eq__(self, o: object) -> bool:
        return True if self.__dict__ == o.__dict__ else False

    # def __repr__(self) -> str:
    #     pass

if __name__ == "__main__":
    print(Character(first_name="Adam"))
    print(Character(age=15))
    print(Character().__dict__)


# to do
# name, skills, characteristics properties
# repr
# types for skills