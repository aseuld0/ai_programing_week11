# 성적 CSV 검사 프로그램

## ① 무엇을 하나요 (What)

성적 CSV 파일을 읽어 유효한 이름과 점수를 정리하고, 건너뛴 행의 줄 번호와 이유를 기록합니다.

## ② 왜 만들었나요 (Why)

실습용 성적 CSV에는 점수가 비어 있거나 0~100점 범위를 벗어난 행이 섞여 있었습니다. 파일을 읽을 때 유효한 성적은 저장하고, 건너뛴 행은 줄 번호와 이유를 기록해 나중에 쉽게 확인할 수 있도록 이 프로그램을 만들었습니다.

## ③ 어떻게 쓰나요 (How)

Python이 설치된 Windows에서 이 폴더를 VS Code로 엽니다.
상단 메뉴의 **터미널 → 새 터미널**을 누른 뒤 아래 명령을 실행합니다.

```powershell
py .\load_scores.py scores.csv
```

## ④ 어떻게 테스트하나요

같은 터미널에서 첫 줄로 테스트 도구를 설치하고, 둘째 줄로 기본 테스트를 실행합니다.

```powershell
py -m pip install pytest pytest-cov
py -m pytest .\test_load_scores.py --cov=load_scores --cov-report=term-missing
```

실행 결과

```text
load_scores.py      45      11    76%   55-56, 77-86
8 passed in 0.21s
```

## ⑤ 파일 구성

| 파일 | 하는 일 |
|---|---|
| `load_scores.py` | CSV를 읽고 성적과 오류 행을 정리합니다. |
| `scores.csv` | 정상 데이터와 잘못된 행이 섞인 예제입니다. |
| `empty.csv` | 헤더만 들어 있는 예제입니다. |
| `test_load_scores.py` | 정상·예외·경계값을 확인하는 기본 테스트입니다. |

## ⑥ 만든 사람 · AI를 어디에 썼는지

- 만든 사람 — [정다슬 2026100583]
- AI를 쓴 곳 — 기본 테스트 초안과 A·B 비교 실험용 테스트를 만드는 데 사용했습니다.
- 내가 직접 판단한 것 — VS Code에서 실행한 결과를 바탕으로 통과·실패 사례와 커버리지를 확인했습니다.

## 라이선스

MIT License (`LICENSE` 파일 참고)# ai_programing_week11
