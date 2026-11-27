
import pandas as pd

def 정제(df):
    # 원본 데이터를 보호하기 위해 복사본 생성
    df = df.copy()
    print("정제 전 행 수:", len(df))

    # 1단계: 점수가 비어 있는 행 삭제
    df = df.dropna(subset=["점수"])
    print("결측치 제거 후 행 수:", len(df))

    # 2단계: 모든 열이 동일한 중복 행 제거
    df = df.drop_duplicates()
    print("중복 제거 후 행 수:", len(df))

    # 3단계: 반과 과목의 앞뒤 공백 제거
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    print("공백 제거 후 행 수:", len(df))

    # 4단계: 0~100 범위의 정수 점수만 남기기
    df = df[(df["점수"] >= 0) & (df["점수"] <= 100)
            & (df["점수"] % 1 == 0)].copy()
    df["점수"] = df["점수"].astype(int)
    print("범위 및 정수 검사 후 행 수:", len(df))

    return df

df = pd.read_csv("scores_2026.csv", encoding="utf-8")

clean_df = 정제(df)

print("\n정제된 데이터:")
print(clean_df)
print("반 종류:", sorted(clean_df["반"].unique()))
print("과목 종류:", sorted(clean_df["과목"].unique()))

math_df = clean_df[clean_df["과목"] == "수학"]
print(len(math_df))

result = clean_df[(clean_df["반"] == "1반") & (clean_df["점수"] >= 90)]

print(len(result))

class_avg = clean_df.groupby("반")["점수"].mean()
print(class_avg)

subject_class_avg = clean_df.groupby(["과목", "반"])["점수"].mean()
print(subject_class_avg)

result = clean_df.groupby("반")["점수"].agg(["count", "mean", "median", "max"]).round(2)
result.columns = ["개수", "평균", "중앙값", "최댓값"]
print(result)

def 반별평균(df):
    stats = df.groupby("반")["점수"].agg(
        개수="count",
        평균="mean",
        중앙값="median",
        최댓값="max"
    ).round(2)

    print(stats)
    return stats["평균"].to_dict()

print(반별평균(clean_df))

# 개수 일치 검증
print("전체 행 수:", len(clean_df))
print("반별 개수 합:", clean_df.groupby("반")["점수"].count().sum())

# 합계 일치 검증
print("전체 점수 합:", clean_df["점수"].sum())
print("반별 점수 합:", clean_df.groupby("반")["점수"].sum().sum())

# 1반 수학 점수 확인
check = clean_df[(clean_df["반"] == "1반") & (clean_df["과목"] == "수학")]

print("1반 수학 점수:", check["점수"].tolist())
print("점수 합:", check["점수"].sum())
print("개수:", len(check))
print("직접 계산한 평균:", check["점수"].sum() / len(check))