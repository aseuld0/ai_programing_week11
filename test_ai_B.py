"""load_scores()의 명세를 검사하는 pytest 테스트."""

import builtins
import errno
import io
import re
from pathlib import Path

import pytest

from load_scores import load_scores


@pytest.fixture
def make_csv(tmp_path):
    """각 테스트에 사용할 임시 CSV 파일을 만든다."""
    def write_csv(contents):
        path = tmp_path / "scores.csv"
        path.write_text(contents, encoding="utf-8", newline="")
        return path

    return write_csv


def assert_skipped(skipped, expected):
    """기록에 들어 있는 줄 번호와 사유를 확인한다."""
    assert len(skipped) == len(expected)
    for (line_no, _original_row, reason), (expected_line, reason_pattern) in zip(
        skipped, expected
    ):
        assert line_no == expected_line
        assert re.search(reason_pattern, reason), (
            f"{line_no}행의 제외 사유가 예상과 다릅니다. 실제 사유는 {reason!r}입니다."
        )


def test_reads_valid_rows_in_file_order(make_csv):
    path = make_csv("name,score\n이보람,85\n김하나,72\n")

    assert load_scores(path) == ([("이보람", 85), ("김하나", 72)], [])


def test_reads_quoted_name_with_comma(make_csv):
    path = make_csv('name,score\n"최,네번",77\n')

    assert load_scores(path) == ([("최,네번", 77)], [])


def test_header_only_returns_empty_lists(make_csv):
    assert load_scores(make_csv("name,score\n")) == ([], [])


@pytest.mark.parametrize("score", [0, 100], ids=["minimum", "maximum"])
def test_accepts_score_at_boundary(make_csv, score):
    path = make_csv(f"name,score\n김하나,{score}\n")

    kept, skipped = load_scores(path)

    assert kept == [("김하나", score)]
    assert type(kept[0][1]) is int
    assert skipped == []


@pytest.mark.parametrize(
    ("bad_row", "reason_pattern"),
    [
        pytest.param("김하나,-1", r"범위|0.*100|range", id="below-minimum"),
        pytest.param("김하나,101", r"범위|0.*100|range", id="above-maximum"),
        pytest.param("김하나,3.5", r"정수|integer", id="decimal-score"),
        pytest.param("김하나,abc", r"정수|integer", id="text-score"),
        pytest.param("김하나,", r"점수.*(비어|빈|누락)|missing score", id="empty-score"),
        pytest.param(",82", r"이름.*(비어|빈|누락)|missing name", id="empty-name"),
        pytest.param("김하나", r"열|column", id="too-few-columns"),
        pytest.param("김하나,82,기타", r"열|column", id="too-many-columns"),
    ],
)
def test_skips_invalid_row_and_keeps_reading(make_csv, bad_row, reason_pattern):
    path = make_csv(f"name,score\n이보람,90\n{bad_row}\n서한별,95\n")

    kept, skipped = load_scores(path)

    assert kept == [("이보람", 90), ("서한별", 95)]
    assert_skipped(skipped, [(3, reason_pattern)])


def test_keeps_only_first_valid_row_for_duplicate_name(make_csv):
    path = make_csv("name,score\n김하나,68\n이보람,82\n김하나,95\n")

    kept, skipped = load_scores(path)

    assert kept == [("김하나", 68), ("이보람", 82)]
    assert_skipped(skipped, [(4, r"중복|duplicate")])


def test_invalid_row_does_not_reserve_name(make_csv):
    path = make_csv("name,score\n김하나,101\n김하나,80\n")

    kept, skipped = load_scores(path)

    assert kept == [("김하나", 80)]
    assert_skipped(skipped, [(2, r"범위|0.*100|range")])


def test_records_file_line_number_after_multiline_name(make_csv):
    path = make_csv('name,score\n"김\n하나",90\n이보람,101\n서한별,95\n')

    kept, skipped = load_scores(path)

    assert kept == [("김\n하나", 90), ("서한별", 95)]
    assert_skipped(skipped, [(4, r"범위|0.*100|range")])


def test_raises_if_file_does_not_exist(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_raises_if_file_cannot_be_read(make_csv, monkeypatch):
    path = make_csv("name,score\n김하나,80\n")
    original_open = builtins.open

    def deny_open(file, *args, **kwargs):
        if not isinstance(file, int) and Path(file) == path:
            raise PermissionError(errno.EACCES, "Permission denied", str(path))
        return original_open(file, *args, **kwargs)

    # 운영체제와 실행 계정에 관계없이 같은 읽기 오류를 재현한다.
    monkeypatch.setattr(builtins, "open", deny_open)
    monkeypatch.setattr(io, "open", deny_open)

    with pytest.raises(PermissionError):
        load_scores(path)


@pytest.mark.parametrize(
    "contents",
    [
        pytest.param("student,points\n김하나,82\n", id="wrong-header"),
        pytest.param("score,name\n82,김하나\n", id="reversed-header"),
        pytest.param("", id="missing-header"),
    ],
)
def test_rejects_file_without_required_header(make_csv, contents):
    # 명세에 헤더 오류의 예외 종류가 없어 ValueError로 정했다.
    with pytest.raises(ValueError):        
        load_scores(make_csv(contents))