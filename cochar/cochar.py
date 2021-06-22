"""Call of Cthulhu character generator
"""
import random
import os
import json
import randname
from bisect import bisect_left
from utils import OCCUPATIONS_GROUPS, OCCUPATIONS_LIST

POP_PIRAMID_PATH = os.path.abspath(os.path.join('data', 'popPiramid.json'))

AGE_RANGE = (
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
YEAR_RANGE = (1950, 1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995, 2000,
              2005, 2010, 2015, 2020)


class Character():
    _MIN_AGE = 15
    _MAX_AGE = 90
    __SEX_OPTIONS = ['M', 'F', None]
    OCCUPATIONS_GROUPS = OCCUPATIONS_GROUPS.copy()
    OCCUPATIONS_LIST = OCCUPATIONS_LIST.copy()

    def __init__(
            self,
            year: int = 1925,
            age: str = None,
            sex: str = None,
            first_name: str = None,
            last_name: str = None,
            country: str = "US",
            occupation: str = None,
            occupation_mode: str = "optimal",
            weights: bool = True) -> None:
        self._year = year
        if sex in self.__SEX_OPTIONS:
            self._sex = self.set_sex(sex)
        else:
            raise ValueError("incorrect sex falue: sex -> ['M', 'F', None']") 
        self._age = self.set_age(age)
        self._country = country
        self._weights = weights
        # personals
        self._first_name = randname.first_name(self._year, self._sex, self._country, self._weights) if not first_name else first_name
        self._last_name = randname.first_name(self._year, self._sex, self._country, self._weights) if not last_name else last_name
        # characteristics
        self._str = 0
        self._con = 0
        self._siz = 0
        self._dex = 0
        self._app = 0
        self._edu = 0
        self._int = 0
        self._pow = 0
        self._move_rate = 0
        self._set_characteristics()
        # derived atributes
        self._sanity_points = 0
        self._magic_points = 0
        self._hit_points = 0
        self._luck = 0
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
        
        self.skill_points_groups = (
            self._edu * 4,                  # 1
            self._edu * 2 + self._pow * 2,  # 2
            self._edu * 2 + self._dex * 2,  # 3
            self._edu * 2 + self._app * 2,  # 4
            self._edu * 2 + self._str * 2,  # 5
        )

        self._occupation = self.get_occupation(self._occupation)
        # self.occupation_points = self.get_skill_points(self._occupation)

    @property
    def year(self):
        return self._year
    
    @property
    def sex(self):
        return self._sex
    
    @property
    def age(self):
        return self._age

    @property
    def country(self):
        return self._country
    
    @property
    def weights(self):
        return self._weights

    @property
    def occupation(self):
        return self._occupation

    @sex.setter
    def sex(self, new_sex):
        if new_sex in ['M', 'F', None]:
            self._sex = self.set_sex(new_sex)
        else:
            raise ValueError("incorrect sex falue: sex -> ['M', 'F', None']")

    @age.setter
    def age(self, new_age):
        if self._MIN_AGE <= new_age <= self._MAX_AGE:
            self._age = new_age
        else:
            raise ValueError(f"age not in range: [{self._MIN_AGE}, {self._MAX_AGE}]")

    @occupation.setter
    def occupation(self, new_occupation):
        # TO DO
        self._occupation = new_occupation
    
    @staticmethod
    def set_sex(sex):
        """Set character Sex

        :param sex: new sex
        :type sex: [type]
        :return: [description]
        :rtype: [type]
        """
        if sex is None:
            return random.choice(['M', 'F'])
        else:
            return sex.upper()

    def set_age(self, age=None):
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
                self.age = random.randint(*age_range)
            return self.age
        else:
            self.age = age
            return self.age

    def _set_characteristics(self):
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

    def _set_derived_attributes(self):
        # Warning! First use add_characteristics method
        self._sanity_points = self._pow
        self._magic_points = self._pow // 5
        self._hit_points = (self._siz + self._con) // 10
        self._luck = random.randint(15, 90)

        if self.age <= 19:
            self._luck = max(self._luck, random.randint(15, 90))

    def _substract_characteristics_points(self, mod_points=None, char='', points=0):
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

    def _characteristic_test(self, attr_name, count):
        characteristic_value = getattr(self, attr_name)
        for _ in range(count):
            test = random.randint(1, 100)
            if characteristic_value < test:
                characteristic_value += random.randint(1, 10)
        setattr(self, attr_name, characteristic_value)

    def _correct_move_rate(self, count):
        if self._dex < self._siz and self._str < self._siz:
            self._move_rate = 7
        elif self._str >= self._siz and self._dex >= self._siz:
            self._move_rate = 9
        else:
            self._move_rate = 8

        self._move_rate -= count

    def get_occupation(self, occupation):
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

    # def get_skill_points(self, occupation: str):
    #     group_index = [
    #         index for index, group in enumerate(self.OCCUPATIONS_GROUPS) if occupation in group
    #     ]
    #     points = [self.skill_points_groups[i] for i in group_index]

    #     return max(points)


    def __str__(self) -> str:
        return f"""
        Character:
            First name: {self._first_name}
            Last name:  {self._last_name}
        """

    def __eq__(self, o: object) -> bool:
        pass

    def __repr__(self) -> str:
        pass

if __name__ == "__main__":
    print(Character(first_name="Adam"))
    print(Character(age=15))
    print(Character().__dict__)