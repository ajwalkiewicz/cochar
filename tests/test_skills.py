import pytest
from unittest.mock import patch

import cochar
import cochar.skill
import cochar.interface


@pytest.fixture(scope="function", autouse=False)
def skills_interface():
    return cochar.interface.SkillsJSONInterface(cochar.SKILLS_DATABASE, cochar.ERA)


def test_skill_test():
    with patch("random.randint", lambda x, y: 2):
        assert cochar.skill.skill_test(1, 1) == 3

    with patch("random.randint", lambda x, y: 96):
        assert cochar.skill.skill_test(100, 1) == 196


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
            },
            200,
        ),
    ],
)
def test_calc_skill_points(
    tested_input,
    points,
):
    assert cochar.skill.calc_skill_points(**tested_input) == points


@pytest.mark.parametrize(
    "input_skills,output_skills",
    [
        ({"accounting": 5, "acting": 100}, {"acting": 100}),
        ({"anthropology": 1}, {}),  # skills < default
        ({"electrical repair": 10}, {}),  # skills == default
        ({"library use": 100}, {"library use": 100}),  # skills > default
        ({"language (own)": 60}, {"language (own)": 60}),
        ({"language (german)": 1}, {"language (german)": 1}),
        ({"language (german)": 0}, {}),
    ],
)
def test_filter_skills(input_skills, output_skills, skills_interface):
    assert (
        cochar.skill.SkillsGenerator(skills_interface)._filter_skills(input_skills)
        == output_skills
    )


def test_filter_skills_doge_language_own(skills_interface):
    skills_generator = cochar.skill.SkillsGenerator(skills_interface)
    skills_generator.skills_data["language (own)"] = 60
    skills_generator.skills_data["doge"] = 60
    assert skills_generator._filter_skills({"language (own)": 60, "doge": 60}) == {}


@pytest.mark.parametrize(
    "args,output_skills",
    [
        ([1, ["doge"], {}], {"doge": 1}),
        ([1, ["non existing skill"], {}], {"non existing skill": 2}),
        ([100, ["doge"], {}], {"doge": 0}),  # TODO: fix this edge case
        ([100, ["electronics"], {}], {"electronics": 90}),  # That's good case
        ([0, [], {}], {}),
        ([0, ["doge", "nothing"], {}], {"doge": 0, "nothing": 1}),
        ([0, [], {"doge": 0, "nothing": 1}], {"doge": 0, "nothing": 1}),
    ],
)
def test_assign_skill_points(args, output_skills, skills_interface):
    assert (
        cochar.skill.SkillsGenerator(skills_interface)._assign_skill_points(*args)
        == output_skills
    )


@pytest.mark.parametrize(
    "input_skills,output_skills",
    [
        (["4i"], {"fast talk", "intimidate", "persuade", "psychology"}),
        (["3i"], {"fast talk", "intimidate", "persuade", "psychology"}),
        (["2i"], {"fast talk", "intimidate", "persuade", "psychology"}),
        (["1i"], {"fast talk", "intimidate", "persuade", "psychology"}),
        (["interpersonal"], {"fast talk", "intimidate", "persuade", "psychology"}),
        (
            ["survival"],
            {
                "survival (desert)",
                "survival (sea)",
                "survival (arctic)",
                "survival (jungle)",
                "survival (mountains)",
            },
        ),
        (
            ["5v"],
            {
                "survival (desert)",
                "survival (sea)",
                "survival (arctic)",
                "survival (jungle)",
                "survival (mountains)",
            },
        ),
        (["special"], {"cthulhu mythos"}),
        (["1p"], {"cthulhu mythos"}),
        ([], {}),
    ],
)
def test_category_skills(input_skills, output_skills, skills_interface):
    skills = cochar.skill.SkillsGenerator(skills_interface)._get_category_skills(
        input_skills
    )

    assert set(skills).issubset(output_skills)

    if input_skills:
        if len(input_skills[0]) == 2:
            assert len(skills) == int(input_skills[0][0])
        else:
            assert len(skills) == 1


@pytest.mark.parametrize(
    "input_list,output_skills",
    [
        ([[1, "occult"], "skill"], {"occult"}),
        (
            [[2, "first aid", "mechanical repair", "1i"]],
            {
                "first aid",
                "mechanical repair",
                "fast talk",
                "intimidate",
                "persuade",
                "psychology",
            },
        ),
        ([[1, "occult"], [1, "special"]], {"occult", "cthulhu mythos"}),
        ([], {}),
    ],
)
def test_get_choice_skills(input_list, output_skills, skills_interface):
    assert set(
        cochar.skill.SkillsGenerator(skills_interface)._get_choice_skills(input_list)
    ).issubset(output_skills)


@pytest.mark.parametrize(
    "input_list,output_skills",
    [
        (
            [[1, "occult"], "4i"],
            {"occult", "fast talk", "intimidate", "persuade", "psychology"},
        ),
        ([[1, "occult"], [1, "special"]], {"occult", "cthulhu mythos"}),
        ([[1, "occult"], "1p"], {"occult", "cthulhu mythos"}),
        (
            ["appraise", "history", "library use", "spot hidden"],
            {"appraise", "history", "library use", "spot hidden"},
        ),
        ([], {}),
    ],
)
def test_get_skills_list(input_list, output_skills, skills_interface):
    assert set(
        cochar.skill.SkillsGenerator(skills_interface)._get_skills_list(input_list)
    ).issubset(output_skills)


@pytest.mark.parametrize(
    "occupation,occupation_points",
    [
        ("antiquarian", 0),
        ("antiquarian", 29),
        ("antiquarian", 30),
        ("antiquarian", 31),
        ("antiquarian", 69),
        ("antiquarian", 70),
        ("antiquarian", 71),
    ],
)
def test_generate_credit_rating_points_one_example(occupation, occupation_points):
    # For antiquarian standard range is [30, 70]
    credit_rating = cochar.skill.generate_credit_rating_points(
        occupation, occupation_points
    )
    assert 0 <= credit_rating <= occupation_points


def test_generate_credit_rating_points_all_occupations():
    for occupation, item in cochar.OCCUPATIONS_DATA.items():
        occupation_credit_rating_range = item["credit_rating"]
        points_to_test = [
            occupation_credit_rating_range[0] - 1
            if occupation_credit_rating_range[0]
            else 0,
            occupation_credit_rating_range[0],
            occupation_credit_rating_range[0] + 1,
            occupation_credit_rating_range[1] - 1,
            occupation_credit_rating_range[1],
            occupation_credit_rating_range[1] + 1,
        ]
        for points in points_to_test:
            credit_rating = cochar.skill.generate_credit_rating_points(
                occupation, points
            )
            assert 0 <= credit_rating <= points
