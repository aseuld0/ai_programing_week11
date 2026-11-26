"""bug3_logic.find_max가 리스트의 최댓값을 반환하는지 확인한다."""

import pytest

from bug3_logic import find_max


def test_returns_maximum_at_first_position():
    assert find_max([95, 70, 85, 60]) == 95


def test_returns_maximum_at_middle_position():
    assert find_max([70, 85, 60, 75]) == 85


def test_returns_maximum_at_last_position():
    assert find_max([70, 85, 60, 95]) == 95


def test_returns_only_score_for_single_item():
    assert find_max([0]) == 0


def test_checks_both_scores_in_two_item_list():
    assert find_max([0, 100]) == 100


def test_raises_index_error_for_empty_scores():
    with pytest.raises(IndexError):
        find_max([])