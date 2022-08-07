import random
from typing import Union, List

import randname
from . import errors
from .skills import Skills
from .settings import *


class Character:
    def __init__(
        self,
        year: int = 0,
        country: str = "",
        first_name: str = "",
        last_name: str = "",
        age: int = 0,
        sex: str = "",
        occupation: str = "",
        strength: int = 0,
        condition: int = 0,
        size: int = 0,
        dexterity: int = 0,
        appearance: int = 0,
        education: int = 0,
        intelligence: int = 0,
        power: int = 0,
        luck: int = 0,
        move_rate: int = 0,
        damage_bonus: str = 0,
        build: int = 0,
        doge: int = 0,
        skills: Skills() = {},
        sanity_points: int = 0,
        magic_points: int = 0,
        hit_points: int = 0,
    ) -> None:
        self.year = year
        self.country = country
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.sex = sex
        self.occupation = occupation
        self.strength = strength
        self.condition = condition
        self.size = size
        self.dexterity = dexterity
        self.appearance = appearance
        self.education = education
        self.intelligence = intelligence
        self.power = power
        self.move_rate = move_rate
        self.luck = luck
        self.damage_bonus = damage_bonus
        self.build = build
        self.skills = Skills(skills)
        self.doge = doge
        self.sanity_points = sanity_points
        self.magic_points = magic_points
        self.hit_points = hit_points

    @property
    def year(self) -> int:
        """**Year of born**

        :raises ValueError: Invalid year. year must be integer
        :return: year
        :rtype: int

        >>> character = create_character()
        >>> character.year = 1800
        """
        return self._year

    @year.setter
    def year(self, new_year: int) -> None:
        if not isinstance(new_year, int):
            raise ValueError(f"Invalid year: {new_year}. year must be integer")
        self._year = new_year

    @property
    def sex(self) -> Union[str, None]:
        """Character sex

        **legend**

        - M: male
        - F: female
        - None: for non binary

        As there is not data for non binary names. When ``None`` is selected sex will be randomly drawn from [M, F]

        :raises ValueError: Incorrect sex value: sex -> ['M', 'F', None']
        :return: sex
        :rtype: Union[str, None]

        >>> c = Character()
        >>> c.sex
        'F'
        """
        return self._sex

    @sex.setter
    def sex(self, new_sex: Union[str, None]) -> None:
        if new_sex in SEX_OPTIONS:
            self._sex = get_sex(new_sex)
        else:
            raise ValueError("Incorrect sex value: sex -> ['M', 'F', None']")

    @property
    def age(self) -> int:
        """**Character age**

        Age has to be between MIN_AGE and MAX_AGE.

        :raises ValueError: Invalid age. Age must be an integer
        :raises ValueError: Age not in range: {new_age} -> [{MIN_AGE}, {MAX_AGE}]
        :return: Character age
        :rtype: int
        """
        return self._age

    @age.setter
    def age(self, new_age: int) -> None:
        if not isinstance(new_age, int):
            raise errors.SkillValueNotAnInt("Invalid age. Age must be an integer")

        if MIN_AGE <= new_age <= MAX_AGE:
            self._age = new_age
        else:
            raise ValueError(f"Age not in range: {new_age} -> [{MIN_AGE}, {MAX_AGE}]")

    @property
    def country(self) -> str:
        """**Character country**

        Country must bu in available countries.

        See ``randname.available_countries()``

        :raises ValueError: "Country not available: {new_country} -> {randname.available_countries()}
        :return: character country
        :rtype: str
        """
        return self._country

    @country.setter
    def country(self, new_country: str) -> None:
        if new_country in randname.available_countries():
            self._country = new_country
        else:
            raise ValueError(
                f"Country not available: {new_country} -> {randname.available_countries()}"
            )

    @property
    def occupation(self) -> str:
        """Character occupation.

        Occupation must be in ``OCCUPATION_LIST``

        :raises ValueError: Occupation: {new_occupation} not in -> {OCCUPATIONS_LIST}
        :return: [description]
        :rtype: str
        """
        return self._occupation

    @occupation.setter
    def occupation(self, new_occupation: str) -> None:
        if new_occupation in OCCUPATIONS_LIST:
            self._occupation = new_occupation
        else:
            raise ValueError(
                f"Occupation: {new_occupation} not in -> {OCCUPATIONS_LIST}"
            )

    @property
    def strength(self) -> int:
        """Character strength

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: character strength
        :rtype: int
        """
        return self._str

    @strength.setter
    def strength(self, new_strength: int) -> None:
        self.__validate_character_properties(new_strength, "strength")
        self._str = new_strength

    @property
    def condition(self) -> int:
        """Character condition.

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: character condition
        :rtype: int
        """
        return self._con

    @condition.setter
    def condition(self, new_condition: int) -> None:
        self.__validate_character_properties(new_condition, "condition")
        self._con = new_condition

    @property
    def size(self) -> int:
        """Character size

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: character size
        :rtype: int
        """
        return self._siz

    @size.setter
    def size(self, new_size: int) -> None:
        self.__validate_character_properties(new_size, "size")
        self._siz = new_size

    @property
    def dexterity(self) -> int:
        """Character dexterity

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: character dexterity
        :rtype: int
        """
        return self._dex

    @dexterity.setter
    def dexterity(self, new_dexterity: int) -> None:
        self.__validate_character_properties(new_dexterity, "dexterity")
        self._dex = new_dexterity

    @property
    def appearance(self) -> int:
        """Character appearance

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: character appearance
        :rtype: int
        """
        return self._app

    @appearance.setter
    def appearance(self, new_appearance: int) -> None:
        self.__validate_character_properties(new_appearance, "appearance")
        self._app = new_appearance

    @property
    def education(self) -> int:
        """Character education

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: character education
        :rtype: int
        """
        return self._edu

    @education.setter
    def education(self, new_education: int) -> None:
        self.__validate_character_properties(new_education, "education")
        self._edu = new_education

    @property
    def intelligence(self) -> int:
        """Character intelligence

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: character intelligence
        :rtype: int
        """
        return self._int

    @intelligence.setter
    def intelligence(self, new_intelligence: int) -> None:
        self.__validate_character_properties(new_intelligence, "intelligence")
        self._int = new_intelligence

    @property
    def power(self) -> int:
        """Character power

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: character power
        :rtype: int
        """
        return self._pow

    @power.setter
    def power(self, new_power: int) -> None:
        self.__validate_character_properties(new_power, "power")
        self._pow = new_power

    @property
    def move_rate(self) -> int:
        """Character move rate

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: character move rate
        :rtype: int
        """
        return self._move_rate

    @move_rate.setter
    def move_rate(self, new_move_rate: int) -> None:
        self.__validate_character_properties(new_move_rate, "move rate")
        self._move_rate = new_move_rate

    @property
    def first_name(self) -> str:
        """Character first name

        :raises ValueError: Invalid first name. Name cannot be an empty string
        :return: first name
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, new_first_name: str) -> None:
        if new_first_name == "":
            raise ValueError("Invalid first name. Name cannot be an empty string")
        self._first_name = str(new_first_name)

    @property
    def last_name(self) -> str:
        """Character last name

        :raises ValueError: Invalid last name. Name cannot be an empty string
        :return: last name
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, new_last_name: str) -> None:
        if new_last_name == "":
            raise ValueError("Invalid last name. Name cannot be an empty string")
        self._last_name = str(new_last_name)

    @property
    def occupation_points(self) -> int:
        """Character occupation points

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: occupation points
        :rtype: int
        """
        return self._occupation_points

    @occupation_points.setter
    def occupation_points(self, new_occupation_points: int) -> None:
        self.__validate_character_properties(new_occupation_points, "occupation")
        self._occupation_points = new_occupation_points

    @property
    def hobby_points(self) -> int:
        """Character hobby points

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: hobby points
        :rtype: int
        """
        return self._hobby_points

    @hobby_points.setter
    def hobby_points(self, new_hobby_points: int) -> None:
        self.__validate_character_properties(new_hobby_points, "hobby")
        self._hobby_points = new_hobby_points

    @property
    def sanity_points(self) -> int:
        """Character sanity points

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: sanity points
        :rtype: int
        """
        return self._sanity_points

    @sanity_points.setter
    def sanity_points(self, new_sanity_points: int) -> None:
        self.__validate_character_properties(new_sanity_points, "sanity")
        self._sanity_points = new_sanity_points

    @property
    def magic_points(self) -> int:
        """Character magic points

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: magic points
        :rtype: int
        """
        return self._magic_points

    @magic_points.setter
    def magic_points(self, new_magic_points: int) -> None:
        self.__validate_character_properties(new_magic_points, "magic")
        self._magic_points = new_magic_points

    @property
    def hit_points(self) -> int:
        """Character hit points

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: hit points
        :rtype: int
        """
        return self._hit_points

    @hit_points.setter
    def hit_points(self, new_hit_points: int) -> None:
        self.__validate_character_properties(new_hit_points, "hit")
        self._hit_points = new_hit_points

    @property
    def luck(self) -> int:
        """Character luck

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: luck
        :rtype: int
        """
        return self._luck

    @luck.setter
    def luck(self, new_luck: int) -> None:
        self.__validate_character_properties(new_luck, "luck")
        self._luck = new_luck

    @property
    def skills(self) -> Skills:
        return self._skills

    @skills.setter
    def skills(self, new_skills: Union[dict, Skills]) -> None:
        if isinstance(new_skills, Skills):
            self._skills = new_skills    
        elif isinstance(new_skills, dict):
            self._skills = Skills(new_skills)
        else: 
            raise errors.SkillsNotADict("Invalid skills. Skills must be a dict")
        

    @property
    def damage_bonus(self) -> str:
        """Character damage bonus

        ``correct_values = ['-2', '-1', '0', '+1K4', '+1K6', '+2K6', '+3K6', '+4K6', '+5K6']``

        :raises ValueError: Invalid damage bonus. {new_damage_bonus} not in {correct_values}
        :return: damage bonus
        :rtype: str
        """
        return self._damage_bonus

    @damage_bonus.setter
    def damage_bonus(self, new_damage_bonus: str) -> None:
        # TODO: Increase range. +1 for each 80 point above STR+SIZ
        correct_values = [
            "-2",
            "-1",
            "0",
            "+1K4",
            "+1K6",
            "+2K6",
            "+3K6",
            "+4K6",
            "+5K6",
        ]
        new_damage_bonus = str(new_damage_bonus).upper()
        if new_damage_bonus in correct_values:
            self._damage_bonus = new_damage_bonus
        else:
            raise ValueError(
                f"Invalid damage bonus. {new_damage_bonus} not in {correct_values}"
            )

    @property
    def build(self) -> int:
        """Character build

        ``correct_values = [-2, -1, 0, 1, 2, 3, 4, 5, 6]``

        TODO: increase range. +1 for each 80 point above STR+SIZ

        :raises ValueError: Invalid build. {new_build} not in {correct_values}
        :return: build
        :rtype: int
        """
        return self._build

    @build.setter
    def build(self, new_build: int) -> None:
        # TODO: increase range. +1 for each 80 point above STR+SIZ
        correct_values = [-2, -1, 0, 1, 2, 3, 4, 5, 6]
        if new_build in correct_values:
            self._build = new_build
        else:
            raise ValueError(f"Invalid build. {new_build} not in {correct_values}")

    @property
    def doge(self) -> int:
        """Character doge

        Doge is also one of the character skills.
        Changing this value changes also ``skills['doge']``.
        But it doesn't work vice versa.

        :raises ValueError: if variable is not an integer
        :raises ValueError: if variable is below 0
        :return: doge
        :rtype: int
        """
        return self._doge

    @doge.setter
    def doge(self, new_doge: int) -> None:
        self.__validate_character_properties(new_doge, "doge")
        self._skills["doge"] = new_doge
        self._doge = new_doge

    @staticmethod
    def __validate_character_properties(new_variable: int, variable_name: str) -> None:
        """Private function to validate in setters whether new_variable
        is a correct one.

        :param new_variable: variable to check
        :type new_variable: int
        :param variable_name: name of that variable
        :type variable_name: str
        :raises SkillValueNotAnInt: if variable is not an integer
        :raises SkillValueNotAnInt: if variable is below 0

        >>> Character._Character__validate_character_properties("a", 'luck')
        errors.SkillValueNotAnInt: Invalid luck points. Luck points must be an integer
        >>> Character._Character__validate_character_properties(-1, 'luck')
        errors.SkillValueNotAnInt: Luck points cannot be less than 0
        """
        variable_name = str(variable_name)
        if not isinstance(new_variable, int):
            raise errors.SkillValueNotAnInt(
                f"Invalid {variable_name.lower()} points. {variable_name.capitalize()} points must be an integer: {new_variable}"
            )
        if new_variable < 0:
            raise ValueError(
                f"{variable_name.capitalize()} points cannot be less than 0"
            )

    def __eq__(self, o: object) -> bool:
        return True if self.__dict__ == o.__dict__ else False

    def __repr__(self) -> str:
        return f"Character(year={self._year}, country='{self._country}', first_name='{self._first_name}', last_name='{self._last_name}', age={self._age}, sex='{self._sex}', occupation='{self._occupation}', strength={self._str}, condition={self._con}, size={self._siz}, dexterity={self._dex}, appearance={self._app}, education={self._edu}, intelligence={self._int}, power={self._pow}, move_rate={self._move_rate}, luck={self._luck}, skills={self._skills}, damage_bonus='{self._damage_bonus}', build={self._build}, doge={self._doge}, sanity_points={self._sanity_points}, magic_points={self._magic_points}, hit_points={self._hit_points})"

    def __str__(self) -> str:
        skills = ""
        max_items_in_row = 3
        current_number_of_items_in_row = 0
        for skill, value in self._skills.items():
            if current_number_of_items_in_row == max_items_in_row:
                skills += "\n"
                current_number_of_items_in_row = 0
            skills += f"| {skill.capitalize()}: {value} |"
            current_number_of_items_in_row += 1
        return f"""Character
Name: {self._first_name} {self._last_name} 
Sex: {self._sex}, Age: {self._age}, Country: {self._country} 
Occupation: {self._occupation.capitalize()} 
STR: {self._str} CON: {self._con} SIZ: {self._siz} 
DEX: {self._dex} APP: {self._app} EDU: {self._edu}
INT: {self._int} POW: {self._pow} Luck: {self._luck}
Damage bonus: {self._damage_bonus}
Build: {self._build}
Doge: {self._doge}
Move rate: {self._move_rate}
Skills:
{skills}
"""


def get_sex(sex: Union[str, bool]) -> str:
    return random.choice(["M", "F"]) if sex is False else sex.upper()
