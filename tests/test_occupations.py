#!/usr/bin/python3
import pytest

import cochar
import cochar.occup
import cochar.error


def test_get_occupation_list():
    assert set(cochar.occup.get_occupation_list()) == set(cochar.OCCUPATIONS_LIST)


@pytest.mark.parametrize(
    "intelligence,hobby_points,points",
    [
        (100, None, 200),
        (100, 50, 50),
        (50, 0, 100),
        (0, 0, 0),
        (0, None, 0),
    ],
)
def test_calc_hobby_points(intelligence, hobby_points, points):
    assert cochar.occup.calc_hobby_points(intelligence, hobby_points) == points


@pytest.mark.parametrize(
    "tested_input,points",
    [
        (
            {
                "occupation": "professor",
                "education": 50,
                "power": 0,
                "dexterity": 0,
                "appearance": 0,
                "strength": 0,
                "occupation_points": None,
            },
            200,
        ),
        (
            {
                "occupation": "artist",
                "education": 50,
                "power": 50,
                "dexterity": 0,
                "appearance": 0,
                "strength": 0,
                "occupation_points": None,
            },
            200,
        ),
        (
            {
                "occupation": "artist",
                "education": 50,
                "power": 0,
                "dexterity": 50,
                "appearance": 0,
                "strength": 0,
                "occupation_points": None,
            },
            200,
        ),
        (
            {
                "occupation": "athlete",
                "education": 50,
                "power": 0,
                "dexterity": 0,
                "appearance": 0,
                "strength": 50,
                "occupation_points": None,
            },
            200,
        ),
        (
            {
                "occupation": "entertainer",
                "education": 50,
                "power": 0,
                "dexterity": 0,
                "appearance": 50,
                "strength": 0,
                "occupation_points": None,
            },
            200,
        ),
        (
            {
                "occupation": "entertainer",
                "education": 50,
                "power": 0,
                "dexterity": 0,
                "appearance": 50,
                "strength": 0,
                "occupation_points": 500,
            },
            500,
        ),
        (
            {
                "occupation": "entertainer",
                "education": 50,
                "power": 0,
                "dexterity": 0,
                "appearance": 50,
                "strength": 0,
                "occupation_points": 0,
            },
            0,
        ),
    ],
)
def test_calc_occupation_points(
    tested_input,
    points,
):
    assert cochar.occup.calc_occupation_points(**tested_input) == points


def test_generate_occupation_random():
    o = cochar.occup.generate_occupation(random_mode=True)
    assert o in cochar.OCCUPATIONS_LIST


def test_generate_occupation_with_occupation():
    occupation = cochar.occup.generate_occupation(occupation="criminal")
    assert occupation == "criminal"


def test_generate_occupation_tags():
    occupation = cochar.occup.generate_occupation(tags=["criminal"])
    assert occupation in ["gangster boss", "criminal"]
    assert occupation not in ["drifter"]


def test_generate_occupation_occup_type():
    o = cochar.occup.generate_occupation(occup_type="custom")
    assert o == "software tester"


def test_generate_occupation_era():
    o = cochar.occup.generate_occupation(era="modern", occup_type="custom")
    # TODO: improve in future, when there will be more modern occupation than just one
    assert o == "software tester"


def test_generate_occupation_value_error():
    with pytest.raises(cochar.error.NoneOccupationMeetsCriteria):
        cochar.occup.generate_occupation(era="modern", tags=["lovecraftian"])


@pytest.mark.parametrize(
    "input_data, occupation",
    [
        (
            {
                "education": 1,
                "power": 1,
                "dexterity": 1,
                "appearance": 1,
                "strength": 1,
                "random_mode": False,
                "occupation": "hacker",
                "occup_type": None,
                "era": None,
                "tags": None,
            },
            "hacker",
        ),
        (
            {
                "education": 1,
                "power": 1,
                "dexterity": 1,
                "appearance": 1,
                "strength": 1,
                "random_mode": False,
                "occupation": None,
                "occup_type": "custom",
                "era": ["modern"],
                "tags": None,
            },
            "software tester",
        ),
    ],
)
def test_generate_occupation(input_data, occupation):
    assert cochar.occup.generate_occupation(**input_data) == occupation


def test_generate_occupation_lovecraftian():
    assert cochar.occup.generate_occupation(education=90, tags=["lovecraftian"]) in [
        "author",
        "librarian",
        "dilettante",
        "doctor of medicine",
        "journalist",
        "professor",
    ]


def test_generate_occupation_random():
    assert cochar.occup.generate_occupation(random_mode=True) in cochar.OCCUPATIONS_LIST


def test_generate_occupation_incorrect_occupation():
    with pytest.raises(cochar.error.IncorrectOccupation):
        cochar.occup.generate_occupation(occupation="Doesn't exist")


@pytest.fixture
def xfail_selected_combinations(request):
    occup_type = request.getfixturevalue("occup_type")
    era = request.getfixturevalue("era")
    tags = request.getfixturevalue("tags")

    allowed_failures = [
        ("classic", ["classic-1920"], ["lovecraftian"]),
        ("classic", ["classic-1920"], ["criminal"]),
        ("expansion", ["classic-1920"], ["criminal"]),
        ("classic", ["classic-1890", "classic-1920", "modern"], ["criminal"]),
        ("classic", ["classic-1890", "classic-1920", "modern"], ["lovecraftian"]),
        ("expansion", ["classic-1890", "classic-1920", "modern"], ["criminal"]),
    ]
    if (occup_type, era, tags) in allowed_failures:
        request.node.add_marker(pytest.mark.xfail(reason="Work as intended"))


@pytest.mark.parametrize("occup_type", ["classic", "expansion", "custom"])
@pytest.mark.parametrize(
    "era",
    [
        ["classic-1890"],
        ["classic-1920"],
        ["modern"],
        ["classic-1890", "classic-1920", "modern"],
    ],
)
@pytest.mark.parametrize("tags", [["lovecraftian"], ["criminal"], ["None"]])
@pytest.mark.usefixtures("xfail_selected_combinations")
def test_generate_occupation_none_occupation_meets_criteria(occup_type, era, tags):
    with pytest.raises(cochar.error.NoneOccupationMeetsCriteria):
        cochar.occup.generate_occupation(occup_type=occup_type, era=era, tags=tags)
