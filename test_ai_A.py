import pytest

from load_scores import load_scores


@pytest.fixture
def write_csv(tmp_path):
    """각 테스트가 사용할 임시 CSV 파일을 만든다."""
    def write(contents):
        path = tmp_path / "scores.csv"
        path.write_text(contents, encoding="utf-8")
        return path

    return write


def test_loads_valid_rows_in_order(write_csv):
    path = write_csv('name,score\n  김하나  , 88 \n"최,네번",77\n윤보람,64\n')

    assert load_scores(path) == ([("김하나", 88), ("최,네번", 77), ("윤보람", 64)], [])


def test_keeps_both_rows_with_same_name(write_csv):
    path = write_csv("name,score\n김하나,88\n김하나,92\n")

    assert load_scores(path) == ([("김하나", 88), ("김하나", 92)], [])


def test_missing_file_raises_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_header_only_returns_empty_lists(write_csv):
    path = write_csv("name,score\n")

    assert load_scores(path) == ([], [])


def test_accepts_score_boundaries(write_csv):
    path = write_csv("name,score\n최저점,0\n최고점,100\n")

    assert load_scores(path) == ([("최저점", 0), ("최고점", 100)], [])


@pytest.mark.parametrize(
    ("invalid_row", "reason"),
    [
        pytest.param("김하나", "열 개수가 2가 아님", id="too-few-columns"),
        pytest.param("김하나,88,추가", "열 개수가 2가 아님", id="too-many-columns"),
        pytest.param("김하나,", "점수가 비어 있음", id="empty-score"),
        pytest.param("김하나,   ", "점수가 비어 있음", id="whitespace-score"),
        pytest.param("김하나,abc", "점수가 정수가 아님", id="text-score"),
        pytest.param("김하나,88.5", "점수가 정수가 아님", id="decimal-score"),
        pytest.param("김하나,-1", "점수가 0~100 밖", id="below-minimum"),
        pytest.param("김하나,101", "점수가 0~100 밖", id="above-maximum"),
        pytest.param(",88", "이름이 비어 있음", id="empty-name"),
        pytest.param("   ,88", "이름이 비어 있음", id="whitespace-name"),
    ],
)
def test_records_invalid_row_and_continues(write_csv, invalid_row, reason):
    path = write_csv(f"name,score\n김가람,70\n{invalid_row}\n윤보람,64\n")

    kept, skipped = load_scores(path)

    assert kept == [("김가람", 70), ("윤보람", 64)]
    assert skipped == [(3, invalid_row, reason)]


def test_ignores_blank_lines_and_keeps_line_numbers(write_csv):
    path = write_csv("name,score\n\n김하나,88\n\n윤보람,\n")

    assert load_scores(path) == (
        [("김하나", 88)],
        [(5, "윤보람,", "점수가 비어 있음")],
    )
