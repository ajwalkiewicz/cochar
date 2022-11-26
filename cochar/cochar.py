"""**Cochar - main module**"""
import json
import random
from typing import List, Tuple, Union

import randname

import cochar
import cochar.character
import cochar.occup
import cochar.skill
import cochar.utils
import cochar.error

cochar.set_logging_level("debug")


# TODO: write unit test
def create_character(
    year: int,
    country: str,
    first_name: str = False,
    last_name: str = False,
    age: int = False,
    sex: str = False,
    random_mode: bool = False,
    occupation: str = None,
    skills: cochar.skill.Skills = {},
    *args,
    **kwargs,
) -> cochar.character.Character:
    """Main function for creating Character.
    Use this function instead of instantiating Character class.

    :param year: year of the game
    :type year: int
    :param country: country of character's origin
    :type country: str
    :param first_name: character's first name, defaults to ""
    :type first_name: str, optional
    :param last_name: character's last name, defaults to ""
    :type last_name: str, optional
    :param age: character's age, defaults to False
    :type age: int, optional
    :param sex: character's sex, defaults to False
    :type sex: str, optional
    :param random_mode: choose occupation completely randomly, regardless the character's statistics, defaults to "False"
    :type random_mode: bool, optional
    :param occupation: character's occupation return provided occupation as character's occupation if it exists, defaults to "None"
    :type occupation: str, optional
    :param skills: character's skills, defaults to {}
    :type skills: Skills, optional
    :raises ValueError: raise if sex is incorrect
    :return: generated character
    :rtype: Character
    """
    weights = cochar.WEIGHTS

    if is_sex_valid(sex):
        sex = generate_sex(sex)
    else:
        raise ValueError(f"incorrect sex value: {sex} -> ['M', 'F', None']")

    age: int = generate_age(year, sex, age)

    if not first_name:
        first_name = generate_first_name(year, sex, country, weights)
    else:
        first_name = first_name

    if not last_name:
        last_name = generate_last_name(year, sex, country, weights)
    else:
        last_name = last_name

    (
        strength,
        condition,
        size,
        dexterity,
        appearance,
        education,
        intelligence,
        power,
        luck,
        move_rate,
    ) = generate_base_characteristics(age=age)

    occupation = cochar.occup.generate_occupation(
        education=education,
        power=power,
        dexterity=dexterity,
        appearance=appearance,
        strength=strength,
        random_mode=random_mode,
        occupation=occupation,
    )

    sanity_points, magic_points, hit_points = calc_derived_attributes(
        power, size, condition
    )

    # TODO: analyze doge flow
    damage_bonus, build, doge = calc_combat_characteristics(strength, size, dexterity)

    occupation_points = cochar.occup.calc_occupation_points(
        occupation, education, power, dexterity, appearance, strength
    )
    hobby_points = cochar.occup.calc_hobby_points(intelligence)
    skills = cochar.skill.generate_skills(
        occupation, occupation_points, hobby_points, dexterity, education, skills
    )

    doge = skills.get("doge", doge)

    return cochar.character.Character(
        year=year,
        country=country,
        first_name=first_name,
        last_name=last_name,
        age=age,
        sex=sex,
        occupation=occupation,
        strength=strength,
        condition=condition,
        size=size,
        dexterity=dexterity,
        appearance=appearance,
        education=education,
        intelligence=intelligence,
        power=power,
        luck=luck,
        damage_bonus=damage_bonus,
        build=build,
        move_rate=move_rate,
        skills=skills,
        doge=doge,
        sanity_points=sanity_points,
        magic_points=magic_points,
        hit_points=hit_points,
    )


# TODO: write unit test
def generate_age(year, sex, age: int = False) -> int:
    """Set age

    :param age: new age, defaults to None
    :type age: int, optional
    :return: new age
    :rtype: int
    """
    if age:
        return age

    if year < 1950:
        corrected_year = 1950
    else:
        year_index = cochar.utils.narrowed_bisect(cochar.utils.YEAR_RANGE, year)
        corrected_year = cochar.utils.YEAR_RANGE[year_index]

    file_name = f"pop{corrected_year}"

    with open(cochar.POP_PYRAMID_PATH, "r", encoding="utf-8") as json_file:

        def correct_age_range(age_range: Tuple[int, int], max_age: int):
            for i, elem in enumerate(age_range):
                if elem[1] > max_age:
                    return i
            return len(age_range) + 1

        max_age_index = correct_age_range(cochar.utils.AGE_RANGE, cochar.MAX_AGE)
        age_population = cochar.utils.AGE_RANGE[:max_age_index]

        age_weights = json.load(json_file)[file_name][sex][3 : 3 + max_age_index]
        age_range = random.choices(age_population, weights=age_weights)[0]

        age = random.randint(*age_range)

    return age


# TODO: write unit test
def generate_base_characteristics(
    age,
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
) -> tuple:
    """Return base characteristics based on age as a tuple.

    Base characteristics:
    1. strength
    2. condition
    3. size
    4. dexterity
    5. appearance
    6. education
    7. intelligence
    8. power
    9. luck
    10. move rate

    :param age: character's age
    :type age: int
    :param strength: strength, defaults to 0
    :type strength: int, optional
    :param condition: condition, defaults to 0
    :type condition: int, optional
    :param size: size, defaults to 0
    :type size: int, optional
    :param dexterity: dexterity, defaults to 0
    :type dexterity: int, optional
    :param appearance: appearance, defaults to 0
    :type appearance: int, optional
    :param education: education, defaults to 0
    :type education: int, optional
    :param intelligence: intelligence, defaults to 0
    :type intelligence: int, optional
    :param power: power, defaults to 0
    :type power: int, optional
    :param move_rate: move rate, defaults to 0
    :type move_rate: int, optional
    :param luck: luck, defaults to 0
    :type luck: int, optional
    :return: (strength, condition, size, dexterity, appearance, education, intelligence, power, luck, move_rate)
    :rtype: tuple
    """
    if strength == 0:
        strength = random.randint(15, 90)
    if condition == 0:
        condition = random.randint(15, 90)
    if size == 0:
        size = random.randint(40, 90)
    if dexterity == 0:
        dexterity = random.randint(15, 90)
    if appearance == 0:
        appearance = random.randint(15, 90)
    if education == 0:
        education = random.randint(40, 90)
    if intelligence == 0:
        intelligence = random.randint(40, 90)
    if power == 0:
        power = random.randint(15, 90)
    if move_rate == 0:
        move_rate = 0
    if luck == 0:
        luck = random.randint(15, 90)
    if age <= 19:
        luck = max(luck, random.randint(15, 90))

    age_range = cochar.utils.narrowed_bisect(cochar.MODIFIERS["age_range"], age)
    mod_char_points = cochar.MODIFIERS["mod_char_points"][age_range]
    mod_app = cochar.MODIFIERS["mod_app"][age_range]
    mod_move_rate = cochar.MODIFIERS["mod_move_rate"][age_range]
    mod_edu = cochar.MODIFIERS["mod_edu"][age_range]

    appearance = subtract_points_from_characteristic(appearance, mod_app)
    strength, condition, dexterity = subtract_points_from_str_con_dex(
        strength, condition, dexterity, mod_char_points
    )
    education = characteristic_test(education, mod_edu)
    move_rate = calc_move_rate(strength, dexterity, size) - mod_move_rate

    return (
        strength,
        condition,
        size,
        dexterity,
        appearance,
        education,
        intelligence,
        power,
        luck,
        move_rate,
    )


# TODO: write unit test
def calc_derived_attributes(
    power: int,
    size: int,
    condition: int,
    sanity_points: int = 0,
    magic_points: int = 0,
    hit_points: int = 0,
) -> Tuple[int, int, int]:
    """Based on power, size and condition,
    return sanity, magic and hit points

    :param power: power points
    :type power: int
    :param size: size points
    :type size: int
    :param condition: condition points
    :type condition: int
    :param sanity_points: sanity points, defaults to 0
    :type sanity_points: int, optional
    :param magic_points: magic points, defaults to 0
    :type magic_points: int, optional
    :param hit_points: hit points, defaults to 0
    :type hit_points: int, optional
    :return: (sanity points, magic points, hit points)
    :rtype: tuple
    """
    if sanity_points == 0:
        sanity_points = calc_sanity_points(power)
    if magic_points == 0:
        magic_points = calc_magic_points(power)
    if hit_points == 0:
        hit_points = calc_hit_points(size, condition)

    return sanity_points, magic_points, hit_points


def calc_sanity_points(power: int) -> int:
    """Return sanity points based on power

    :param power: power value
    :type power: int
    :return: sanity points
    :rtype: int
    """
    return power


def calc_magic_points(power: int) -> int:
    """Return magic points based on power

    :param power: power value
    :type power: int
    :return: magic points
    :rtype: int
    """
    return power // 5


def calc_hit_points(size: int, condition: int) -> int:
    """Return hit points based on size and condition.

    :param size: size value
    :type size: int
    :param condition: condition value
    :type condition: int
    :return: hit points
    :rtype: int
    """
    return (size + condition) // 10


# TODO: write unit test
def calc_combat_characteristics(
    strength: int,
    size: int,
    dexterity: int,
    damage_bonus: str = "",
    build: int = 0,
    doge: int = 0,
) -> Tuple[str, int, int]:
    """Based on strength, size and dexterity,
    return combat characteristics such as:
    dame bonus, build, doge

    :param strength: strength points
    :type strength: int
    :param size: size points
    :type size: int
    :param dexterity: dexterity points
    :type dexterity: int
    :return: (damage bonus, build, doge)
    :rtype: Tuple(str, int, int)
    """
    if damage_bonus == "":
        damage_bonus = calc_damage_bonus(strength, size)
    if build == 0:
        build = calc_build(strength, size)
    if doge == 0:
        doge = calc_doge(dexterity)

    return damage_bonus, build, doge


# TODO: write unit test
def calc_damage_bonus(strength: int, size: int) -> str:
    """Return damage bonus, based on sum of strength and size.

    f: X -> Y

    X: {64, 84, 124, 164, 204, 283, 364, 444, 524}
    Y: {"-2", "-1", "0", "+1K4", "+1K6", "+2K6", "+3K6", "+4K6", "+5K6",}

    TODO: Increase bonus damage for +1K6 for every 80 points above 524

    :param strength: character's strength
    :type strength: int
    :param size: character's size
    :type size: int
    :return: character's damage bonus
    :rtype: str
    """
    sum_str_siz = strength + size
    combat_range = cochar.utils.narrowed_bisect(
        cochar.VALUE_MATRIX["combat_range"], sum_str_siz
    )
    damage_bonus = cochar.VALUE_MATRIX["damage_bonus"][combat_range]
    return damage_bonus


# TODO: write unit test
def calc_build(strength: int, size: int) -> int:
    """Return build based on sum od strength and size.

    f: X -> Y

    X: {64, 84, 124, 164, 204, 283, 364, 444, 524}
    Y: {-2, -1, 0, 1, 2, 3, 4, 5, 6}

    TODO: Increase bonus damage for +1K6 for every 80 points above 524

    :param strength: character's strength
    :type strength: int
    :param size: character's size
    :type size: int
    :return: character's build
    :rtype: int
    """
    sum_str_siz = strength + size
    combat_range = cochar.utils.narrowed_bisect(
        cochar.VALUE_MATRIX["combat_range"], sum_str_siz
    )
    build = cochar.VALUE_MATRIX["build"][combat_range]
    return build


def calc_doge(dexterity: int) -> int:
    """Return doge based on dexterity:

    doge = dexterity // 2

    :param dexterity: character's dexterity
    :type dexterity: int
    :return: character's doge
    :rtype: int
    """
    return dexterity // 2


# TODO: write unit test
def subtract_points_from_characteristic(
    characteristic_points: int, subtract_points: int
) -> int:
    """Subtract points from characteristic points,
    but if result would be zero or below, than return 1.

    :param characteristic_points: _description_
    :type characteristic_points: int
    :param subtract_points: _description_
    :type subtract_points: int
    :return: _description_
    :rtype: int

    >>> education = 50
    >>> points_to_subtract = 10
    >>> subtract_points_from_characteristic(education, points_to_subtract)
    40
    >>> points_to_subtract = 60
    >>> subtract_points_from_characteristic(education, points_to_subtract)
    1
    """
    return (
        characteristic_points - subtract_points
        if characteristic_points > subtract_points
        else 1
    )


# TODO: write unit test
def subtract_points_from_str_con_dex(
    strength: int, condition: int, dexterity: int, subtract_points: int
) -> Tuple[int, int, int]:
    """Subtract certain amount of points from strength, condition and
    dexterity, but but prevent each of the characteristics to be
    lower than 1.

    :param strength: character's strength
    :type strength: int
    :param condition: character's condition
    :type condition: int
    :param dexterity: character's dexterity
    :type dexterity: int
    :param subtract_points: amount of points to subtract
    :type subtract_points: int
    :return: (strength, condition, dexterity)
    :rtype: Tuple[int, int, int]
    """
    strength = strength
    condition = condition
    dexterity = dexterity
    for _ in range(subtract_points):
        characteristic_to_subtract = [
            characteristic
            for characteristic in (strength, condition, dexterity)
            if characteristic != 1
        ]
        if characteristic_to_subtract:
            characteristic = random.choice(characteristic_to_subtract)
            characteristic = characteristic - 1
        else:
            break

    return strength, condition, dexterity


# TODO: write unit test
def characteristic_test(tested_value: int, repetition: int = 1) -> int:
    """Perform characteristic test.

    TODO: Double check if that works this way for characteristics.
    Works like improvement test. Roll number between 1 to 100,
    If that number is higher than tested value or higher
    then 95, than increase tested value with random number,
    between 1 to 10.

    Repeat repetition times.

    .. note:
        for skills use skill_test()

    :param tested_value: tested value
    :type tested_value: int
    :param repetition: how many test to perform
    :type repetition: int
    :return: unchanged or increased tested value
    :rtype: int
    """
    for _ in range(repetition):
        test = random.randint(1, 100)
        if tested_value < test:
            tested_value += random.randint(1, 10)
    return tested_value


# TODO: write unit test
def calc_move_rate(strength: int, dexterity: int, size: int) -> int:
    """Return move rate base on relations between
    strength, dexterity and size

    if both dexterity and strength are smaller than size,
    return 7
    if both strength and size are higher or equal than size,
    return 9
    else return 8

    :param strength: character's strength
    :type strength: int
    :param dexterity: characters dexterity
    :type dexterity: int
    :param size: character's size
    :type size: int
    :return: move rate
    :rtype: int
    """
    if dexterity < size and strength < size:
        move_rate = 7
    elif strength >= size and dexterity >= size:
        move_rate = 9
    else:
        move_rate = 8

    return move_rate


# TODO: write unit test
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


# TODO: write unit test
def generate_last_name(year: int, sex: str, country: str, weights: bool) -> str:
    """Return random last name based on the given parameters

    .. note:
        For generating only last name, use randname module.

    :param year: year of the data set with names (if data set not available use a closes available data set)
    :type year: int
    :param sex: name gender, available options ['M', 'F', 'N', None]
    :type sex: str
    :param country: name country
    :type country: str
    :param weights: If true, take under account popularity of names. [default: True]
    :type weights: bool
    :return: last name
    :rtype: str
    """
    sex = verify_and_return_sex(sex, country, name="last_names")
    return randname.last_name(
        year,
        sex,
        country,
        weights,
        database=cochar.DATABASE,
        show_warnings=cochar.SHOW_WARNINGS,
    )


# TODO: write unit test
def generate_first_name(year: int, sex: str, country: str, weights: bool) -> str:
    """Return random first name based on given parameters.

    .. note:
        For generating only first name, use randname module.

    :param year: year of the data set with names (if data set not available use a closes available data set)
    :type year: int
    :param sex: name gender, available options ['M', 'F', 'N', None]
    :type sex: str
    :param country: name country
    :type country: str
    :param weights: if true, take under account popularity of names. [default: True]
    :type weights: bool
    :return: first name
    :rtype: str
    """
    # TODO: Fix capitalization for Spanish first names
    sex = verify_and_return_sex(sex, country, name="first_names")
    return randname.first_name(
        year,
        sex,
        country,
        weights,
        database=cochar.DATABASE,
        show_warnings=cochar.SHOW_WARNINGS,
    )


# TODO: write unit test
# TODO: investigate sex flow
def verify_and_return_sex(sex: str, country: str, name: str) -> str:
    """Return valid sex, based on sex, country and name.
    if provided sex is invalid, it will be overridden, and
    function return valid sex.

    :param sex: _description_
    :type sex: str
    :param country: _description_
    :type country: str
    :param name: _description_
    :type name: str
    :return: _description_
    :rtype: str
    """
    available_sex = randname.show_data()[country][name]
    if sex not in available_sex:
        if "N" in available_sex:
            sex = "N"
        else:
            sex = random.choice(available_sex)
    return sex


# TODO: consider refactoring sex functions
# TODO: write unit test
def is_sex_valid(sex: str) -> bool:
    """Return True if sex is valid, else False

    :param sex: character's sex
    :type sex: str
    :return: True|False
    :rtype: bool
    """
    return True if sex in cochar.SEX_OPTIONS else False


# TODO: write unit test
def generate_sex(sex: Union[str, bool]) -> str:
    """Get sex

    TODO: investigate sex workflow. Why there is no sex verification here
    TODO: add unit tests for sex

    :param sex: character's sex
    :type sex: Union[str, bool]
    :return: sex
    :rtype: str
    """
    return random.choice(("M", "F")) if sex is False else sex.upper()
