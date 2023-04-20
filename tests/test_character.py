import pytest

import cochar
import cochar.character


@pytest.fixture
def example_characters_json():
    return [
        {
            "year": 1925,
            "country": "US",
            "first_name": "Oswaldo",
            "last_name": "Hammack",
            "age": 50,
            "sex": "M",
            "occupation": "farmer",
            "strength": 69,
            "condition": 51,
            "size": 81,
            "dexterity": 30,
            "appearance": 17,
            "education": 57,
            "intelligence": 63,
            "power": 33,
            "move_rate": 5,
            "luck": 65,
            "damage_bonus": "+1K4",
            "build": 1,
            "skills": {
                "natural world": 51,
                "operate heavy machinery": 41,
                "track": 61,
                "psychology": 74,
                "throw": 86,
                "firearms (handgun)": 31,
                "firearms (rifle shotgun)": 26,
                "sleight of hand": 12,
                "spot hidden": 81,
                "stealth": 26,
                "science (pharmacy)": 41,
                "credit rating": 10,
            },
            "dodge": 15,
            "sanity_points": 33,
            "magic_points": 6,
            "hit_points": 13,
        },
        {
            "year": 1925,
            "country": "US",
            "first_name": "Zanaya",
            "last_name": "Krohn",
            "age": 25,
            "sex": "F",
            "occupation": "police detective",
            "strength": 67,
            "condition": 50,
            "size": 79,
            "dexterity": 26,
            "appearance": 43,
            "education": 45,
            "intelligence": 83,
            "power": 31,
            "move_rate": 7,
            "luck": 55,
            "damage_bonus": "+1K4",
            "build": 1,
            "skills": {
                "listen": 51,
                "psychology": 27,
                "spot hidden": 83,
                "firearms (handgun)": 52,
                "fast talk": 6,
                "operate heavy machinery": 86,
                "science (pharmacy)": 51,
                "credit rating": 46,
            },
            "dodge": 13,
            "sanity_points": 31,
            "magic_points": 6,
            "hit_points": 12,
        },
    ]


def test_year_bigger_that_range():
    c = cochar.create_character(year=2022, country="US")
    assert c.year == 2022


def test_get_json_format(example_characters_json):
    for character in example_characters_json:
        c = cochar.character.Character(**character)
        assert character == c.get_json_format()
