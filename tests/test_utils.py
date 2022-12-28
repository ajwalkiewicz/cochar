import pytest

import cochar.utils


@pytest.mark.parametrize(
    "a,x,result",
    [
        ([0, 1, 2], -1, 0),
        ([0, 1, 2], 0, 0),
        ([0, 1, 2], 1, 1),
        ([0, 1, 2], 2, 2),
        ([0, 1, 2], 3, 2),
    ],
)
def test_narrowed_bisect(a, x, result):
    assert cochar.utils.narrowed_bisect(a, x) == result


@pytest.mark.parametrize(
    "skill_value,result",
    [
        ("1", False),
        (-1, False),
        (1, True),
    ],
)
def test_is_skill_valid(skill_value, result):
    assert cochar.utils.is_skill_valid(skill_value) == result
