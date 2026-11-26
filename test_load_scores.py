from pathlib import Path

import pytest

from load_scores import load_scores


DATA_DIR = Path(__file__).resolve().parent


def test_정상_파일을_읽는다():
    kept, skipped = load_scores(DATA_DIR / "scores.csv")

    assert kept == [
        ("김하나", 88),
        ("최,네번", 77),
        ("김하나", 91),
        ("윤보람", 64),
        ("서한별", 95),
    ]
    assert len(skipped) == 5


def test_빈_줄은_기록_없이_건너뛴다(tmp_path):
    path = tmp_path / "blank_line.csv"
    path.write_text("name,score\n김하나,88\n\n윤보람,64\n", encoding="utf-8")

    assert load_scores(path) == ([("김하나", 88), ("윤보람", 64)], [])


def test_이름에_쉼표가_있어도_읽는다(tmp_path):
    path = tmp_path / "quoted_name.csv"
    path.write_text('name,score\n"최,네번",77\n', encoding="utf-8")

    assert load_scores(path) == ([("최,네번", 77)], [])


def test_없는_파일이면_오류가_난다(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_헤더만_있으면_빈_결과가_나온다():
    assert load_scores(DATA_DIR / "empty.csv") == ([], [])


@pytest.mark.parametrize("score, valid", [(0, True), (100, True), (101, False)])
def test_점수_경계값(tmp_path, score, valid):
    path = tmp_path / "boundary.csv"
    path.write_text(f"name,score\n김하나,{score}\n", encoding="utf-8")

    kept, skipped = load_scores(path)

    if valid:
        assert kept == [("김하나", score)]
        assert skipped == []
    else:
        assert kept == []
        assert skipped == [(2, f"김하나,{score}", "점수가 0~100 밖")]